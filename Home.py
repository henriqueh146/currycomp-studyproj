import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon='🎲️',
    layout='wide'
)
#######################################################################################
##                                   Sidebar                                         ##
#######################################################################################

image = 'images/curry.png'

st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown("## Fastest Delivery in Town")

st.sidebar.markdown("""---""")
st.sidebar.markdown("## Powered by Comunidade DS")


#######################################################################################
##                                    Layout                                         ##
#######################################################################################

st.write("## Curry Company Growth Dashboard")

st.markdown(

    """
    Groth Dashboard foi construído para acompanhar métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar este Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for help
    - Time de Data Science
        - @henrique
    """
)