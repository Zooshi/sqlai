import streamlit as st
from database import init_database
from llm import LLMManager

# Page config
st.set_page_config(
    page_title="SQL Generator",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if "schema_info" not in st.session_state:
    st.session_state.schema_info = None

def main():
    st.title("SQL Generator")
    
    # Database connection
    try:
        servername = #fill
        database = #fill
        driver = #fill
        connection_string = #fill
        db_manager = init_database(connection_string)
        
        # Get schema info if not already in session state
        if st.session_state.schema_info is None:
            st.session_state.schema_info = db_manager.get_schema_info()
            
        # Initialize LLM
        llm_manager = LLMManager()
        
        # User input
        query = st.text_area(
            "Enter your query in natural language:",
            placeholder="Example: Show all orders from the last 30 days",
            height=100
        )
        
        if st.button("Generate SQL", type="primary"):
            if query:
                with st.spinner("Generating SQL..."):
                    # Format schema for LLM
                    schema_context = db_manager.format_schema_for_llm(st.session_state.schema_info)
                    
                    # Generate SQL
                    sql_statement = llm_manager.generate_sql(query, schema_context)
                    
                    # Display result
                    st.code(sql_statement, language="sql")
                    
                    # Copy button
                    st.button(
                        "📋 Copy SQL",
                        on_click=lambda: st.write(st.clipboard(sql_statement))
                    )
            else:
                st.warning("Please enter a query first.")
        
        # Display available tables (collapsible)
        with st.expander("Available Tables"):
            for table, columns in st.session_state.schema_info.items():
                st.subheader(f"📊 {table}")
                for col in columns:
                    st.text(f"  ├─ {col['name']} ({col['type']})")
                    
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        st.info("Please ensure your MS SQL Server is running and accessible.")

if __name__ == "__main__":
    main()
