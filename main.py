import google.generativeai as genai
import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

class CustomerSupportAssistant:
    def __init__(self):
        self.setup_gemini()
        self.setup_ui()
        
    def setup_gemini(self):
        """Configure Gemini API"""
        # Read API key from environment variables (from .env)
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY") or os.getenv("GEMINI_KEY")
        if not api_key:
            st.error("❌ Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
            st.stop()
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        self.chat = self.model.start_chat(history=[])
        
    def setup_ui(self):
        """Setup Streamlit UI"""
        st.set_page_config(
            page_title="Customer Support AI 🤖",
            page_icon="💬",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .chat-message.user {
            background-color: #2b313e;
            margin-left: 25%;
        }
        .chat-message.assistant {
            background-color: #475063;
            margin-right: 25%;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.title("💬 Customer Support AI Assistant")
        st.markdown("""
        **Welcome to our 24/7 AI Customer Support!**  
        
        ✅ Answer FAQs instantly  
        ✅ Troubleshoot common issues  
        ✅ Provide product information  
        ✅ Collect feedback  
        
        *How can I help you today?*
        """)
        
    def get_company_context(self):
        """Return company-specific context for the AI"""
        return """
        You are a Customer Support AI Agent for "TechSolutions Inc." - a technology company that provides:
        - Software development services
        - Cloud computing solutions
        - IT consulting
        - Digital transformation services

        Company Information:
        - Support Hours: 24/7
        - Email: support@techsolutions.com
        - Phone: +1-800-TECH-HELP
        - Website: www.techsolutions.com

        Common Services:
        1. Web Development (Starting at $5,000)
        2. Mobile App Development (Starting at $8,000)
        3. Cloud Migration (Starting at $10,000)
        4. IT Consulting ($150/hour)
        5. Maintenance & Support (Monthly plans available)

        Policies:
        - Free initial consultation
        - 30-day money-back guarantee on projects
        - 24/7 emergency support for enterprise clients
        - Standard response time: 2 business hours

        Always be:
        - Professional and friendly
        - Clear and concise
        - Helpful and solution-oriented
        - Empathetic to customer concerns

        If you don't know something, offer to connect them with human support.
        """
    
    def get_gemini_response(self, prompt):
        """Get response from Gemini API with company context"""
        try:
            company_context = self.get_company_context()
            
            full_prompt = f"""{company_context}

            Current Conversation:
            {self.get_conversation_history()}

            User's latest message: {prompt}

            Please provide a helpful, professional response.
            """
            
            response = self.chat.send_message(full_prompt)
            return response.text
            
        except Exception as e:
            return f"❌ Sorry, I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
    
    def get_conversation_history(self):
        """Get recent conversation history for context"""
        if "messages" not in st.session_state:
            return "No previous conversation."
        
        history = ""
        for msg in st.session_state.messages[-6:]:  # Last 6 messages
            role = "Customer" if msg["role"] == "user" else "Support Agent"
            history += f"{role}: {msg['content']}\n"
        
        return history
    
    def handle_special_commands(self, message):
        """Handle special commands"""
        message_lower = message.lower().strip()
        
        if message_lower == "/clear":
            self.chat = self.model.start_chat(history=[])
            if "messages" in st.session_state:
                st.session_state.messages = []
            return "🗑️ Conversation history cleared!"
        
        elif message_lower == "/help":
            return """
            **🆘 Available Commands:**
            `/clear` - Clear conversation history  
            `/help` - Show this help message  
            `/services` - List our services  
            `/contact` - Contact information  
            `/pricing` - Pricing information  

            **💡 Example Questions:**
            - "What are your support hours?"  
            - "How do I request a refund?"  
            - "Tell me about your web development services"  
            - "I need help with my account"  
            - "What's your pricing for mobile apps?"  
            """
        
        elif message_lower == "/services":
            return """
            **🛠️ Our Services:**
            1. **Web Development** - Custom websites and web applications
            2. **Mobile App Development** - iOS and Android apps
            3. **Cloud Solutions** - AWS, Azure, Google Cloud migration
            4. **IT Consulting** - Strategic technology advice
            5. **Maintenance & Support** - Ongoing technical support

            *Want details about any specific service? Just ask!*
            """
        
        elif message_lower == "/contact":
            return """
            **📞 Contact Information:**
            - **Email:** support@techsolutions.com
            - **Phone:** +1-800-TECH-HELP (832-4435)
            - **Live Chat:** Available on our website
            - **Address:** 123 Tech Street, Silicon Valley, CA

            **🕐 Support Hours:** 24/7
            """
        
        elif message_lower == "/pricing":
            return """
            **💰 Pricing Overview:**
            - **Web Development:** Starting at $5,000
            - **Mobile Apps:** Starting at $8,000
            - **Cloud Migration:** Starting at $10,000
            - **IT Consulting:** $150/hour
            - **Support Plans:** From $500/month

            *All projects include free consultation and 30-day guarantee!*
            """
        
        return None
    
    def run(self):
        """Run the chat interface"""
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "👋 Hello! Welcome to TechSolutions Customer Support. How can I help you today?"
                }
            ]
        
        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Sidebar with information and tools
        with st.sidebar:
            st.header("🏢 TechSolutions Inc.")
            st.info("""
            **Leading Technology Solutions Provider**  
            - Since 2002 
            - 500+ Clients  
            - 24/7 Support  
            - Global Presence  
            """)
            
            st.header("🛠️ Quick Access")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📋 Services"):
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": self.handle_special_commands("/services")
                    })
                    st.rerun()
                
                if st.button("💰 Pricing"):
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": self.handle_special_commands("/pricing")
                    })
                    st.rerun()
            
            with col2:
                if st.button("📞 Contact"):
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": self.handle_special_commands("/contact")
                    })
                    st.rerun()
                
                if st.button("🆘 Help"):
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": self.handle_special_commands("/help")
                    })
                    st.rerun()
            
            st.header("⚙️ Tools")
            if st.button("🗑️ Clear Chat"):
                self.chat = self.model.start_chat(history=[])
                st.session_state.messages = [
                    {
                        "role": "assistant", 
                        "content": "✅ Chat cleared! How can I help you?"
                    }
                ]
                st.rerun()
        
        # Chat input
        if prompt := st.chat_input("Type your question here..."):
            # Check for special commands
            special_response = self.handle_special_commands(prompt)
            if special_response:
                st.session_state.messages.append({"role": "assistant", "content": special_response})
                st.rerun()
                return
            
            # Display user message
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Get AI response
            with st.spinner("🤔 Thinking..."):
                response = self.get_gemini_response(prompt)
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    assistant = CustomerSupportAssistant()
    assistant.run()
