# import streamlit as st
# import pandas as pd
# import re
# import matplotlib.pyplot as plt
# import seaborn as sns
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Initialize LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash-001",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     google_api_key='AIzaSyCB0nvDatYRZb0Ok8AaB6Jle1AkqbQIvqc'
# )

# st.title("📊 Auto Graph Generator")
# st.write("Upload a dataset and get the best 10 graphs instantly!")

# # File uploader
# uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
    
#     st.subheader("📋 Dataset Preview")
#     st.dataframe(df.head())

#     # Prepare the message for LLM
#     columns = list(df.columns)
#     message = [
#         f'''system: you are an AI assistant that will suggest only graphs types by viewing the dataset content and also write short and complete code to draw all the graphs. dataset columns names are - {columns}

#         human: this is the sample of the dataset values {df.head(2)}
#         note - Plot only 10 best Graphs with equal sizes and there must be same columns name that is provided and not change in indentations and also installation is already done so don't add installation libraries
#          '''
#     ]

#     if st.button("Generate Graphs 🚀"):
#         with st.spinner("Generating graphs..."):
#             response = llm.invoke(message)

#             # Extract code block
#             code_blocks = re.findall(r"```(?:python)?\s*(.*?)```", response.content, re.DOTALL)
#             full_code = "\n".join(code_blocks)

#             st.subheader("🧩 Generated Code")
#             with st.expander("See Generated Code"):
#                 st.code(full_code, language='python')

#             # Safe execution
#             try:
#                 exec_globals = {"df": df, "sns": sns, "plt": plt, "pd": pd}
#                 exec(full_code, exec_globals)
                
#                 st.subheader("📈 Graphs")
#                 # Collect all plt figures
#                 figs = [manager.canvas.figure for manager in plt._pylab_helpers.Gcf.get_all_fig_managers()]
#                 for fig in figs:
#                     st.pyplot(fig)
#             except Exception as e:
#                 st.error(f"Error in executing generated code: {e}")




import streamlit as st
import pandas as pd
import re
import textwrap
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key='AIzaSyCB0nvDatYRZb0Ok8AaB6Jle1AkqbQIvqc'
)

st.title("📊 Auto Graph Generator with AI")
st.write("Upload your dataset and instantly get 10 best graphs!")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head())
    input = st.text_input("input prompt: ", key = "input")

    option = st.selectbox(
    'How would you like to be contacted?',
     ('Scatter', 'line', 'histograph', 'bargraph', 'pie chart'))
    st.write('You selected:', option)

    # Prepare message for LLM
    columns = list(df.columns)
    # message = [
    #     f'''system: you are an AI assistant that will make best fit graph by viewing the dataset content and also write short and complete python code to plot all the graphs. dataset columns names are - {columns} data is already read in df
    #     graphs to plot - Scatter, line, histograph, bargraph, pie chart

    #     human: this is the sample of the dataset values (df.head(2) - {df.head(2)})
    #     note - Plot only 10 best Graphs with equal sizes and there must be same columns name that is provided and not change in indentations and also installation is already done so don't add installation libraries 
    #      '''
    # ]
    message = [
        f'''system: you are an AI assistant that will make best fit graph by viewing the dataset content and also write short and complete python code to plot graphs. dataset columns names are - {columns} data is already read in df.


        human: this is the sample of the dataset values (df.head(2) - {df.head(2)})
        note - this is user input {input} and graph type {option}
        note - Only use matplotlib and seaborn
         '''
    ]

    if st.button("Generate Graphs 🚀"):
        with st.spinner("Generating graphs..."):
            try:
                # Invoke LLM
                response = llm.invoke(message)

                # Extract code block
                code_blocks = re.findall(r"```(?:python)?\s*(.*?)```", response.content, re.DOTALL)
                full_code = "\n".join(code_blocks)

                # Dedent to fix indentation errors
                full_code = textwrap.dedent(full_code)

                st.subheader("🧩 Generated Code")
                with st.expander("See Generated Code"):
                    st.code(full_code, language='python')

                # Prepare safe execution environment
                exec_globals = {"df": df, "sns": sns, "plt": plt, "pd": pd}

                # Execute the generated code
                exec(full_code, exec_globals)

                st.subheader("📈 Generated Graphs")
                # Collect all plt figures
                figs = [manager.canvas.figure for manager in plt._pylab_helpers.Gcf.get_all_fig_managers()]
                for fig in figs:
                    st.pyplot(fig)

            except Exception as e:
                st.error(f"Error during graph generation: {e}")
