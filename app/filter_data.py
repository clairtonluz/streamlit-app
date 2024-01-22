def getFilteredData(df, empresas_select, uf_select, status_select, qtd_palavras_select, data_select):
    df_filtered = df
    if empresas_select != 'TODAS':
        df_filtered = df_filtered[df_filtered['empresa'] == empresas_select]
    if uf_select != 'TODOS':
        df_filtered = df_filtered[df_filtered['UF'] == uf_select]
    if status_select != 'TODOS':
        df_filtered = df_filtered[df_filtered['STATUS'] == status_select]
    df_filtered = df_filtered[
        (df_filtered['QTD_DESCRICAO_PALAVRAS'] >= qtd_palavras_select[0]) &
        (df_filtered['QTD_DESCRICAO_PALAVRAS'] <= qtd_palavras_select[1])
    ]
    if len(data_select) == 2:
        df_filtered = df_filtered[
            (df_filtered['TEMPO'] >= data_select[0]) &
            (df_filtered['TEMPO'] <= data_select[1])
        ]
    return df_filtered