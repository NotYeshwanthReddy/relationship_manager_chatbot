from langchain.prompts import PromptTemplate

# Template to determine appropriate data source
data_source_selection_prompt_template = PromptTemplate(
    input_variables = ["question"],
    template = """We have 3 databases in total. SQL, Vector db and file upload.
SQL contains: Customer Data Table, Transaction Table, Risk Assessment Table, 
Vector db contains: Product Recommendations, Meeting Notes, Knowledgebase.
file upload: any supporting document or file which might be mentioned by the user in their question.
Based on the below question from the user, which source(s) do you think we will contain the information required for generating the answer.
user_question = {question}
"""
)

# Template for formatting answers
get_answer_prompt_template = PromptTemplate(
    input_variables=["question", "data", "datasource"],
    template="""
From the data sources: {datasource}.
We received the following data:
{data}.
Answer the question using provided data: {question}
"""
)

# Template to generate SQL queries based on user questions
sql_query_prompt_template = PromptTemplate(
    input_variables=["question"],
    template="""
The DB structure is as follows:
-- 1. Client Profile Table
CREATE TABLE ClientProfile (
    Client_ID VARCHAR(10) PRIMARY KEY,
    Client_Name VARCHAR(100),
    Industry VARCHAR(50),
    Annual_Revenue BIGINT,
    Risk_Score VARCHAR(10),
    Last_Meeting_Date DATE,
    Preferred_Products VARCHAR(255)
);

-- 2. Transactions Table
CREATE TABLE Transactions (
    Transaction_ID VARCHAR(10) PRIMARY KEY,
    Client_ID VARCHAR(10),
    Date DATE,
    Amount DECIMAL(18, 2),
    Transaction_Type VARCHAR(50),
    Description TEXT,
    FOREIGN KEY (Client_ID) REFERENCES ClientProfile(Client_ID)
);

-- 3. Financial Documents Table
CREATE TABLE FinancialDocuments (
    Document_ID VARCHAR(10) PRIMARY KEY,
    Client_ID VARCHAR(10),
    Document_Type VARCHAR(50),
    Upload_Date DATE,
    Key_Metrics JSON,
    FOREIGN KEY (Client_ID) REFERENCES ClientProfile(Client_ID)
);

-- 4. Product Recommendations Table
CREATE TABLE ProductRecommendations (
    Recommendation_ID SERIAL PRIMARY KEY,
    Client_ID VARCHAR(10),
    Recommended_Product VARCHAR(100),
    Reason TEXT,
    Probability_Score DECIMAL(3, 2),
    FOREIGN KEY (Client_ID) REFERENCES ClientProfile(Client_ID)
);

-- 5. Risk and Alerts Table
CREATE TABLE RiskAlerts (
    Alert_ID VARCHAR(10) PRIMARY KEY,
    Client_ID VARCHAR(10),
    Alert_Date DATE,
    Alert_Type VARCHAR(50),
    Description TEXT,
    FOREIGN KEY (Client_ID) REFERENCES ClientProfile(Client_ID)
);

-- 6. Meeting Notes Table
CREATE TABLE MeetingNotes (
    Meeting_ID VARCHAR(10) PRIMARY KEY,
    Client_ID VARCHAR(10),
    Date DATE,
    Key_Topics TEXT,
    Next_Steps TEXT,
    FOREIGN KEY (Client_ID) REFERENCES ClientProfile(Client_ID)
);

-- 7. Knowledge Base Table
CREATE TABLE KnowledgeBase (
    Document_ID VARCHAR(10) PRIMARY KEY,
    Title VARCHAR(100),
    Content_Summary TEXT,
    Vector_Embedding JSON
);

-- 8. Chatbot Conversation Templates Table
CREATE TABLE ChatbotTemplates (
    Template_ID VARCHAR(10) PRIMARY KEY,
    Intent VARCHAR(50),
    Response_Template TEXT
);
Translate the following question into a SQL query: {question}.
"""
)
