import ollama

class LLMManager:
    def __init__(self, model_name: str = "qwen2.5"):
        """Initialize LLM manager."""
        self.model_name = model_name
        
    def generate_sql(self, query: str, schema_context: str) -> str:
        """Generate SQL from natural language query using schema context."""
        prompt = f"""Given the following database schema:

{schema_context}

Generate a valid T-SQL statement for this query: "{query}"

Rules:
1. Use only tables and columns that exist in the schema
2. Generate only valid T-SQL syntax for MS SQL Server
3. Include appropriate JOINs if needed
4. Use proper date/time functions for temporal queries
5. Return only the SQL statement, no explanations. Your answer always needs to start with SELECT

SQL Statement:"""

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            stream=False
        )
        
        return response['response'].strip()
