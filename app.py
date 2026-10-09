import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta
from src.database import init_db, insert_record, fetch_records, delete_record, update_record
from src.processing import clean_records, calculate_kpis, INDICATORS, CATEGORIES, CAMPI, SERIES, STATUSES
from src.validation import RecordInput

st.set_page_config(page_title="Gestão de Dados | Ensino Médio Técnico Senac", page_icon="📊", layout="wide")
init_db()

st.title("📊 Gestão de Dados — Ensino Médio Técnico Senac")
st.caption("Painel de acompanhamento de indicadores pedagógicos e de gestão.")

with st.sidebar:
    st.header("Navegação")
    page = st.radio("Selecione uma área", ["Dashboard", "Cadastrar registro", "Consultar e editar", "Exportar dados"])
    st.divider()
    st.caption("Registre apenas dados necessários à gestão. Evite nomes, documentos e informações pessoais de estudantes.")

if page == "Cadastrar registro":
    st.subheader("Novo registro")
    st.write("Preencha os campos abaixo. Os campos de indicador e categoria acompanham a estrutura da planilha de referência.")
    with st.form("new_record", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            record_date = st.date_input("Data de referência", value=date.today())
            campus = st.selectbox("CEP / Unidade", CAMPI)
            indicator = st.selectbox("Indicador", INDICATORS)
        with c2:
            category = st.selectbox("Categoria / detalhamento", CATEGORIES)
            series = st.selectbox("Série / turma", ["Não se aplica"] + SERIES)
            status = st.selectbox("Status", STATUSES)
        with c3:
            value = st.number_input("Valor numérico", min_value=0.0, step=1.0, help="Informe quantidade, percentual ou pontuação conforme o indicador. Registre percentuais de 0 a 100.")
            unit = st.selectbox("Unidade de medida", ["Quantidade", "Percentual (%)", "Pontuação", "Nota", "Outro"])
            source = st.text_input("Fonte / sistema", placeholder="Ex.: Geekie, secretaria escolar")
        notes = st.text_area("Observações (opcional)", placeholder="Contexto relevante para interpretar o indicador.")
        submitted = st.form_submit_button("Salvar registro", type="primary")
    if submitted:
        try:
            payload = RecordInput(
                record_date=record_date.isoformat(), campus=campus, indicator=indicator,
                category=category, series=None if series == "Não se aplica" else series,
                status=status, value=value, unit=unit, source=source.strip(), notes=notes.strip()
            )
            data = payload.model_dump()
            data["record_date"] = payload.record_date.isoformat()
            insert_record(data)
            st.success("Registro salvo com sucesso.")
        except Exception as exc:
            st.error(f"Não foi possível salvar o registro: {exc}")

elif page == "Consultar e editar":
    st.subheader("Consultar registros")
    raw = fetch_records()
    df = clean_records(raw)
    if df.empty:
        st.info("Ainda não há registros. Cadastre o primeiro registro para começar.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            campuses = st.multiselect("Unidade", sorted(df["campus"].dropna().unique()), default=sorted(df["campus"].dropna().unique()))
        with c2:
            indicators = st.multiselect("Indicador", sorted(df["indicator"].dropna().unique()), default=sorted(df["indicator"].dropna().unique()))
        with c3:
            statuses = st.multiselect("Status", sorted(df["status"].dropna().unique()), default=sorted(df["status"].dropna().unique()))
        view = df[df["campus"].isin(campuses) & df["indicator"].isin(indicators) & df["status"].isin(statuses)]
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.caption("Para corrigir ou excluir, selecione um registro pelo ID.")
        ids = view["id"].astype(int).tolist()
        if ids:
            selected_id = st.selectbox("ID do registro", ids)
            row = view[view["id"] == selected_id].iloc[0]
            with st.expander("Editar registro selecionado"):
                with st.form("edit_record"):
                    e1, e2, e3 = st.columns(3)
                    with e1:
                        edit_date = st.date_input("Data", value=pd.to_datetime(row["record_date"]).date(), key="edit_date")
                        edit_campus = st.selectbox("Unidade", CAMPI, index=CAMPI.index(row["campus"]) if row["campus"] in CAMPI else 0)
                        edit_indicator = st.selectbox("Indicador", INDICATORS, index=INDICATORS.index(row["indicator"]) if row["indicator"] in INDICATORS else 0)
                    with e2:
                        edit_category = st.selectbox("Categoria", CATEGORIES, index=CATEGORIES.index(row["category"]) if row["category"] in CATEGORIES else 0)
                        series_opts = ["Não se aplica"] + SERIES
                        current_series = row["series"] if pd.notna(row["series"]) and row["series"] else "Não se aplica"
                        edit_series = st.selectbox("Série", series_opts, index=series_opts.index(current_series) if current_series in series_opts else 0)
                        edit_status = st.selectbox("Status", STATUSES, index=STATUSES.index(row["status"]) if row["status"] in STATUSES else 0)
                    with e3:
                        edit_value = st.number_input("Valor", min_value=0.0, value=float(row["value"]), step=1.0)
                        units = ["Quantidade", "Percentual (%)", "Pontuação", "Nota", "Outro"]
                        edit_unit = st.selectbox("Unidade de medida", units, index=units.index(row["unit"]) if row["unit"] in units else 0)
                        edit_source = st.text_input("Fonte", value="" if pd.isna(row["source"]) else str(row["source"]))
                    edit_notes = st.text_area("Observações", value="" if pd.isna(row["notes"]) else str(row["notes"]))
                    save_edit = st.form_submit_button("Atualizar registro")
                if save_edit:
                    try:
                        data = RecordInput(record_date=edit_date.isoformat(), campus=edit_campus, indicator=edit_indicator,
                            category=edit_category, series=None if edit_series == "Não se aplica" else edit_series,
                            status=edit_status, value=edit_value, unit=edit_unit, source=edit_source.strip(), notes=edit_notes.strip())
                        edit_data = data.model_dump()
                        edit_data["record_date"] = data.record_date.isoformat()
                        update_record(int(selected_id), edit_data)
                        st.success("Registro atualizado. Atualize a página para ver os dados.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Erro ao atualizar: {exc}")
            if st.button("Excluir registro selecionado", type="secondary"):
                delete_record(int(selected_id))
                st.success("Registro excluído.")
                st.rerun()

elif page == "Exportar dados":
    st.subheader("Exportação")
    df = clean_records(fetch_records())
    if df.empty:
        st.info("Não há dados para exportar.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Baixar CSV", df.to_csv(index=False).encode("utf-8-sig"),
                           file_name="gestao_dados_ensino_medio_senac.csv", mime="text/csv")
        st.caption("O CSV contém somente os registros operacionais cadastrados no aplicativo.")

else:
    st.subheader("Dashboard gerencial")
    df = clean_records(fetch_records())
    if df.empty:
        st.info("O banco ainda não possui registros. Acesse **Cadastrar registro** para inserir os primeiros dados.")
        st.markdown("**Indicadores contemplados:** Clubes, NOA, NPS, Evasão, Atendimentos, Rendimento, Geekie, Docentes Geekie, Ocorrências, Inclusão, Formações e Olimpíadas.")
    else:
        min_date = pd.to_datetime(df["record_date"]).min().date()
        max_date = pd.to_datetime(df["record_date"]).max().date()
        with st.sidebar:
            st.subheader("Filtros do dashboard")
            date_range = st.date_input("Período", value=(min_date, max_date), min_value=min_date, max_value=max_date)
            selected_campi = st.multiselect("Unidade", sorted(df["campus"].dropna().unique()), default=sorted(df["campus"].dropna().unique()), key="dash_campi")
            selected_indicators = st.multiselect("Indicador", sorted(df["indicator"].dropna().unique()), default=sorted(df["indicator"].dropna().unique()), key="dash_indicators")
            selected_status = st.multiselect("Status", sorted(df["status"].dropna().unique()), default=sorted(df["status"].dropna().unique()), key="dash_status")
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start, end = date_range
        else:
            start = end = date_range
        filtered = df[
            (pd.to_datetime(df["record_date"]).dt.date >= start) &
            (pd.to_datetime(df["record_date"]).dt.date <= end) &
            df["campus"].isin(selected_campi) &
            df["indicator"].isin(selected_indicators) &
            df["status"].isin(selected_status)
        ]
        kpis = calculate_kpis(filtered)
        a,b,c,d,e = st.columns(5)
        a.metric("Registros", f'{kpis["records"]:,}'.replace(",", "."))
        b.metric("Unidades", kpis["campuses"])
        c.metric("Indicadores", kpis["indicators"])
        d.metric("Valor acumulado", f'{kpis["sum_value"]:,.1f}'.replace(",", "X").replace(".", ",").replace("X", "."))
        e.metric("Média dos valores", f'{kpis["mean_value"]:,.1f}'.replace(",", "X").replace(".", ",").replace("X", "."))
        st.caption("Os KPIs são descritivos dos registros filtrados. Não some indicadores com unidades diferentes para interpretar desempenho; use os gráficos por indicador.")
        left, right = st.columns(2)
        with left:
            st.markdown("##### Evolução temporal")
            trend = filtered.copy()
            trend["Período"] = pd.to_datetime(trend["record_date"]).dt.to_period("M").astype(str)
            trend = trend.groupby(["Período", "indicator"], as_index=False)["value"].mean()
            if not trend.empty:
                fig = px.line(trend, x="Período", y="value", color="indicator", markers=True,
                              labels={"value": "Média do valor", "indicator": "Indicador"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sem dados para o período selecionado.")
        with right:
            st.markdown("##### Comparação por unidade e indicador")
            bars = filtered.groupby(["campus", "indicator"], as_index=False)["value"].mean()
            if not bars.empty:
                fig = px.bar(bars, x="campus", y="value", color="indicator", barmode="group",
                             labels={"campus": "Unidade", "value": "Média do valor", "indicator": "Indicador"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Sem dados para comparar.")
        st.markdown("##### Distribuição por status")
        status_counts = filtered.groupby("status", as_index=False).size().rename(columns={"size":"Registros"})
        if not status_counts.empty:
            fig = px.pie(status_counts, names="status", values="Registros", hole=0.45)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("##### Registros filtrados")
        st.dataframe(filtered.sort_values("record_date", ascending=False), use_container_width=True, hide_index=True)
