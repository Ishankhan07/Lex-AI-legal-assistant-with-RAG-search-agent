import os
import streamlit as st

from rag.pipeline import RAGPipeline
from rag.vector_store import VectorStore
# import shutil
UPLOAD_DIR = os.path.join("data", "User_upload_pdfs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

WEB_KEYWORDS = [
    "latest",
    "recent",
    "today",
    "news",
    "judgement",
    "judgment",
    "supreme court",
    "high court",
    "update",
    "current",
]

st.set_page_config(
    page_title="LexAI",
    page_icon="⚖️",
    layout="wide"
)


@st.cache_resource(show_spinner=False)
def load_pipeline():
    return RAGPipeline()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

# ---------------- Sidebar: PDF upload ----------------
# ---------------- Sidebar ----------------

with st.sidebar:

    st.title("⚖️ LexAI")
    st.caption("Your Legal Research Assistant")

    st.divider()

    st.subheader("📄 Upload PDF")


    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )


    if uploaded_file is not None:


        save_path = os.path.join(
            UPLOAD_DIR,
            uploaded_file.name
        )


        if st.button(
            "📥 Process PDF",
            use_container_width=True
        ):


            try:


                # Save uploaded PDF

                with open(save_path, "wb") as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )


                with st.spinner(
                    "Building Vector Database..."
                ):


                    # Create user PDF vector database

                    store = VectorStore(
                        pdf_folder=UPLOAD_DIR,
                        index_name="user_index.faiss",
                        chunk_name="user_chunks.pkl"
                    )


                    store.build_vector_store()


                    # Reload pipeline

                    st.cache_resource.clear()

                    pipeline = load_pipeline()



                if uploaded_file.name not in st.session_state.processed_files:


                    st.session_state.processed_files.append(
                        uploaded_file.name
                    )


                st.success(
                    "✅ PDF Indexed Successfully"
                )


                st.info(
                    "Now ask questions from your uploaded PDF."
                )


            except Exception as e:


                st.error(
                    f"❌ {e}"
                )



    # Show uploaded files

    if st.session_state.processed_files:


        st.divider()


        st.markdown(
            "### Indexed PDFs"
        )


        for pdf in st.session_state.processed_files:

            st.write(
                f"✅ {pdf}"
            )



    st.divider()



    # Clear only chat

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):


        st.session_state.messages = []


        st.rerun()



    # Reset uploaded PDF and return to KB

    if st.button(
        "🔄 Reset To Knowledge Base",
        use_container_width=True
    ):


        try:


            # Remove uploaded PDFs

            if os.path.exists(UPLOAD_DIR):


                for file in os.listdir(UPLOAD_DIR):


                    file_path = os.path.join(
                        UPLOAD_DIR,
                        file
                    )


                    if os.path.isfile(file_path):

                        os.remove(file_path)



            # Remove user vector database

            user_index = "vector_db/user_index.faiss"

            user_chunks = "vector_db/user_chunks.pkl"



            if os.path.exists(user_index):

                os.remove(user_index)



            if os.path.exists(user_chunks):

                os.remove(user_chunks)



            # Clear session

            st.session_state.messages = []

            st.session_state.processed_files = []



            # Reload original KB

            st.cache_resource.clear()



            st.success(
                "✅ Switched Back To Legal Knowledge Base"
            )


            st.rerun()



        except Exception as e:


            st.error(
                f"❌ {e}"
            )

# ---------------- Load Pipeline ----------------

with st.spinner("Loading LexAI..."):

    pipeline = load_pipeline()


# ---------------- Main Chat ----------------

st.title("⚖️ LexAI")

st.caption(
    "Ask questions about Indian Laws, Judgements and Legal Documents."
)


# Display previous chat

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("source")
        ):

            if message["source"] == "web":

                st.caption("🌐 Source : Tavily Web Search")

            else:

                st.caption("📚 Source : Legal Knowledge Base")


# User Question

question = st.chat_input(
    "Ask LexAI..."
)


if question:

    # Show User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # Detect source

    if any(
        word in question.lower()
        for word in WEB_KEYWORDS
    ):

        source = "web"

    else:

        source = "kb"


    # Generate Answer

    with st.chat_message("assistant"):

        with st.spinner("LexAI is Thinking..."):

            try:

                answer = pipeline.ask(question)

            except Exception as e:

                answer = f"❌ Error : {e}"


        st.markdown(answer)

        if source == "web":

            st.caption("🌐 Source : Tavily Web Search")

        else:

            st.caption("📚 Source : Legal Knowledge Base")


    # Save Chat

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "source": source
        }
    )