def getListEmpresa(df):
    empresas = df['empresa'].dropna().unique()
    empresas.sort()
    empresas = ['TODAS'] + list(empresas)
    return empresas

def getListUfs(df):
    ufs = df['UF'].dropna().unique()
    ufs.sort()
    ufs = ['TODOS'] + list(ufs)
    return ufs

def getListStatus(df):
    status = df['STATUS'].dropna().unique()
    status.sort()
    status = ['TODOS'] + list(status)
    return status

def getMinMaxDate(df):
    min_date = df['TEMPO'].min()
    max_date = df['TEMPO'].max()
    return min_date, max_date

def getMaxQtdPalavras(df):
    df['QTD_DESCRICAO_PALAVRAS'] = df['DESCRICAO'].apply(lambda x: len(x.split(' ')))
    max_qtd_palavras = df['QTD_DESCRICAO_PALAVRAS'].max()
    return max_qtd_palavras