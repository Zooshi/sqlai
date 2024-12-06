from sqlalchemy import create_engine, MetaData, inspect, text
from typing import Dict, List
import streamlit as st
import pyodbc

class DatabaseManager:
    def __init__(self, connection_string: str):
        """Initialize database connection and metadata."""
        self.engine = create_engine(connection_string)
        self.metadata = MetaData()
        
    def get_schema_info(self) -> Dict[str, List[Dict]]:
        """Retrieve schema information for all tables."""
        schema_info = {}
        
        # Use direct SQL query for more reliable schema retrieval
        query = text("""
            SELECT 
                t.TABLE_NAME,
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.IS_NULLABLE
            FROM INFORMATION_SCHEMA.TABLES t
            JOIN INFORMATION_SCHEMA.COLUMNS c 
                ON t.TABLE_NAME = c.TABLE_NAME
            WHERE t.TABLE_TYPE = 'BASE TABLE'
            ORDER BY t.TABLE_NAME, c.ORDINAL_POSITION
        """)
        
        try:
            with self.engine.connect() as conn:
                result = conn.execute(query)
                
                for row in result:
                    table_name = row[0]
                    if table_name not in schema_info:
                        schema_info[table_name] = []
                        
                    schema_info[table_name].append({
                        "name": row[1],
                        "type": row[2],
                        "nullable": row[3] == 'YES'
                    })
                    
            return schema_info
            
        except Exception as e:
            st.error(f"Error retrieving schema: {str(e)}")
            return {}
    
    def format_schema_for_llm(self, schema_info: Dict[str, List[Dict]]) -> str:
        """Format schema information for LLM context."""
        context = []
        for table, columns in schema_info.items():
            table_desc = f"Table: {table}\nColumns:"
            col_desc = [
                f"- {col['name']} ({col['type']}){'?' if col['nullable'] else ''}"
                for col in columns
            ]
            context.extend([table_desc, *col_desc, ""])
        
        return "\n".join(context)

@st.cache_resource
def init_database(connection_string: str) -> DatabaseManager:
    """Initialize database connection with caching."""
    return DatabaseManager(connection_string)
