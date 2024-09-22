from string import Template

resume_template =  Template("""$resume_dic\nGiven the list of resumes above, respond to the given query. If any of the resumes are relevant to the query, answer the query and provide a brief summary of all relevant resumes. If none of the resumes are relevant, state "I don't have relevant data in my knowledgebase.'\n

Query: $query\n""")