import streamlit as st

from interacts.common import display_lang_selector
from interacts.sl_utils import all_labels
from sagas.ofbiz.service_gen import get_service_package, gen_service_stub, proc_service_refs
from sagas.ofbiz.services import OfService as s, search_service, create_service_data_frame

def sidebar():
    cur_lang=display_lang_selector()

def services():
    serv_name = st.text_input("Search services", '')
    if serv_name!='':
        servs=search_service(serv_name)
        for serv in servs:
            pkg=get_service_package(serv)
            if st.button(f"{pkg}/{serv}"):
                try:
                    lines = []
                    gen_service_stub(lines, serv)
                    st.code('\n'.join(lines), language='javascript')
                except ValueError as e:
                    st.markdown(str(e))

                deps = set()
                proc_service_refs(serv, deps)
                st.markdown(f"`dependencies` **{', '.join(deps)}**")

                df=create_service_data_frame(serv)
                st.dataframe(df)

def main():
    sidebar()
    st.subheader("Services")
    services()

if __name__ == '__main__':
    main()

