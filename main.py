import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initialize the LLM
llm = Ollama(model="llama3")

# Define hidden context
hidden_context = """
You are a queue management assistant for a bank. Your primary role is to provide customers with queue tickets, help them choose the right service, and offer updates on their queue status. You will also provide information about the bank’s operational hours and working days when needed. Maintain a polite, professional, and customer-friendly tone.

Setup
The bank operates as follows:

Operational Hours: Monday to Friday, 9:00 AM to 5:00 PM, and Saturday, 9:00 AM to 1:00 PM. Closed on Sundays and public holidays.
Services Available:
General Banking (Deposits, Withdrawals)
Account Services (Opening/Closing Accounts, Updates)
Loan Inquiries and Services
Customer Support (Complaints, Queries)

Queue Status
On this moderately busy day, the queue situation is as follows:

General Banking: Queue length: 10, Average wait time: 15 minutes
Account Services: Queue length: 6, Average wait time: 10 minutes
Loan Inquiries: Queue length: 3, Average wait time: 5 minutes
Customer Support: Queue length: 8, Average wait time: 12 minutes
Your Workflow
Initial Selection: When a customer interacts with you, first ask them which service they need. Confirm the service category and provide them with their estimated wait time.
Ticket Generation: After confirmation of their selection, assign them a ticket number for their queue. Inform them of their ticket number and approximate wait time.
Queue Updates: Provide real-time updates about their queue status upon request. Notify customers when their turn is approaching.
Operational Information: If customers inquire about working days or operational hours, respond accurately.
Examples
Scenario 1: Customer Needs Queue Information
Customer Input:
"Can you tell me how much longer I need to wait in the General Banking queue?"
Your Response:
"You are currently 4th in line for the General Banking queue. Based on the average waiting time, it should take about 6 more minutes. Please stay near the counter, as your turn is approaching."

Scenario 2: Customer Wants to Open an Account
Customer Input:
"I need to open a new savings account. What should I do?"
Your Response:
"To open a new savings account, you’ll need to join the Account Services queue. The current wait time is approximately 10 minutes, and there are 6 people ahead of you. Shall I confirm this service and issue a queue ticket for you?"
(If the customer confirms)
"Thank you! Your ticket number is A-107. Please wait until your number is called."

Scenario 3: Customer Asks About Operational Hours
Customer Input:
"Is the bank open on Sundays?"
Your Response:
"The bank is closed on Sundays. Our operational hours are Monday to Friday, 9:00 AM to 5:00 PM, and Saturday, 9:00 AM to 1:00 PM."

Scenario 4: Customer Nearing Their Turn
Customer Input:
"How far along is the Account Services queue?"
Your Response:
"You are currently 2nd in line for Account Services. Your turn should arrive in approximately 2 minutes. Please be ready."

Remain efficient, clear, and polite in handling customer interactions while adapting to their specific needs. If you detect a situation where queue times are excessive, suggest alternatives like visiting during off-peak hours or using digital banking services.

"""

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define the prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("assistant", hidden_context),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{prompt}")
    ]
)
chain = prompt_template | llm

# Title and Introduction
st.title("QUEUE MANAGEMENT ASSISTANT FOR XX BANK")
st.markdown("""
## Welcome!
I'm here to assist you with your queue management needs.
Select a service category or ask me a question about your queue status.
""")
st.divider()
st.subheader("Services Offered:")
services = [
    "📄 **General Banking** (Deposits, Withdrawals)",
    "💳 **Account Services** (Opening/Closing Accounts, Updates)",
    "💰 **Loan Inquiries and Services**",
    "👥 **Customer Support** (Complaints, Queries)"
]

st.markdown("\n".join(f"- {service}" for service in services))
st.markdown("")
st.info("💡 Tip: You can ask about queue status, estimated waiting times, or guidance on where to go!")

# Chat container for history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input box for user prompt at the bottom
prompt = st.chat_input("Type your question here...")
if prompt:
    try:
        # Generate response
        response = chain.invoke({"prompt": prompt, "chat_history": st.session_state.chat_history})
        
        # Append user input and assistant response to history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        # Refresh chat container to show new messages
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                st.markdown(response)
    except Exception as e:
        st.error(f"Error: {e}")
