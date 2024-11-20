from langchain_community.llms import Ollama
import streamlit as st

# Initialize the LLM
llm = Ollama(model="llama3")

# Streamlit interface
st.title("Chatbot using Llama3 with Hidden Context")

# Define hidden context (can be static or dynamically updated)
hidden_context = (
    "You are a highly knowledgeable assistant capable of providing accurate and concise responses."
)

# User input for the prompt
prompt = st.text_area("Enter your prompt:", placeholder="Ask your question here...")

# Generate response when the button is clicked
if st.button("Generate"):
    if prompt:
        with st.spinner("Generating response..."):
            try:
                # Combine hidden context and user prompt
                full_prompt = f"{hidden_context}\n\n{prompt}"
                
                # Use llm.invoke() to generate a response
                response = llm.invoke(full_prompt)
                
                # Display response
                st.write("### Response:")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt.")
