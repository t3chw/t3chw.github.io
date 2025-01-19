---
layout: post
title: "Unleashing the Power of Agents with the ReAct Framework"
date: 2025-01-19 14:00:00 +0000
categories: [Tech]
tags: [Agent, Langchain, ReAct]
---

---

## **Part 1: Introduction to Agents and Their Importance**

### **What Are Agents?**

Agents are autonomous systems built on top of large language models (LLMs) that can perform **actions**. Unlike LLMs, which respond with static text-based outputs, agents use tools to interact with the real world, making them significantly more powerful.

### **Why Are Agents the Next Big Thing?**
- **Funding:** Over $87 billion invested in 443 companies working on agentic systems.
- **Predictions:** Experts believe humanity is moving towards a future governed by agents.
- **Potential:** Agents can autonomously perform tasks like booking flights, curating curriculums, and more.

### **Example: Flight Booking Agent**
Imagine an agent that:
1. Searches for flights.
2. Chooses the best option.
3. Books the ticket and makes the payment.

Such automation saves time and effort, showcasing the immense potential of agentic systems.

---

## **Part 2: Understanding Agents**

### **How Do Agents Differ from LLMs?**
1. **LLMs:** Generate responses based on user-defined inputs.
2. **Agents:** Combine reasoning with tools to act autonomously.

### **Key Characteristics of Agents:**
1. **Actions:** Agents can execute multi-step tasks.
2. **Tools:** Agents are equipped with tools like search engines, payment gateways, or calculators.

### **Tools as Enablers**
- For example, a flight booking agent requires:
  1. A **search engine** to find flights.
  2. A **payment gateway** to book tickets.

---

## **Part 3: ReAct Framework**

### **What Is the ReAct Framework?**
ReAct stands for **Reasoning + Acting**. It merges the reasoning capabilities of LLMs with the ability to act autonomously, enabling agents to:

1. **Think:** Decide what to do.
2. **Act:** Choose and deploy tools.
3. **Observe:** Evaluate results and iterate.

### **How ReAct Works:**
1. **Thought:** The agent determines the next step.
2. **Action:** It executes the action using a tool.
3. **Observation:** The agent evaluates the results.

### **Example: Converting USD to Euros**
1. **Cycle 1:**
   - **Thought:** "I need to find the MacBook price in USD."
   - **Action:** Use a web search tool to get the price.
   - **Observation:** "The price is $2499."

2. **Cycle 2:**
   - **Thought:** "I need to convert this price to Euros."
   - **Action:** Use a calculator to perform the conversion.
   - **Observation:** "The price in Euros is €2124.15."

### **Takeaway:**
ReAct uses multiple cycles of **Thought-Action-Observation** to reach accurate results.

---

## **Part 4: Coding Agents Using LangChain**

### **Setting Up the Environment**
1. **Load OpenAI's LLMs with LangChain:**
   ```python
   import os
   from langchain_openai import ChatOpenAI

   os.environ["OPENAI_API_KEY"] = "MY_KEY"
   openai_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
   ```

2. **Create the ReAct Template:**
   ```python
   react_template = """
   Answer the following questions as best you can. You have access to the following tools:

   {tools}

   Use the following format:

   Question: the input question you must answer
   Thought: you should always think about what to do
   Action: the action to take, should be one of [{tool_names}]
   Action Input: the input to the action
   Observation: the result of the action
   ... (this Thought/Action/Action Input/Observation can repeat N times)
   Thought: I now know the final answer
   Final Answer: the final answer to the original input question

   Begin!

   Question: {input}
   Thought:{agent_scratchpad}"""

   from langchain.prompts import PromptTemplate

   prompt = PromptTemplate(
       template=react_template,
       input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
   )
   ```

3. **Integrate Tools:**
   - **Search Tool:** Use DuckDuckGo for web search.
   - **Calculator Tool:** Use the built-in LLM Math tool.

   ```python
   from langchain.agents import load_tools, Tool
   from langchain.tools import DuckDuckGoSearchResults

   # Create search tool
   search = DuckDuckGoSearchResults()
   search_tool = Tool(
       name="duckduck",
       description="A web search engine. Use this to as a search engine for general queries.",
       func=search.run,
   )

   # Prepare tools
   tools = load_tools(["llm-math"], llm=openai_llm)
   tools.append(search_tool)
   ```

4. **Define the ReAct Agent:**
   ```python
   from langchain.agents import AgentExecutor, create_react_agent

   agent = create_react_agent(openai_llm, tools, prompt)
   agent_executor = AgentExecutor(
       agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
   )
   ```

5. **Execute the Agent:**
   ```python
   # Run the agent executor
   agent_executor.invoke(
       {
           "input": "What is the current price of a MacBook Pro in USD? How much would it cost in EUR if the exchange rate is 0.85 EUR for 1 USD?"
       }
   )
   ```

---

## **Part 5: Agent Execution Walkthrough**

### **Execution Steps:**
1. **Cycle 1:**
   - **Thought:** "Find the MacBook price."
   - **Action:** Uses DuckDuckGo to search the web.
   - **Observation:** Finds the price in USD ($2499).

2. **Cycle 2:**
   - **Thought:** "Convert price to Euros."
   - **Action:** Uses the calculator tool.
   - **Observation:** Calculates €2124.15.

### **Final Output:**
"The price of the MacBook Pro is €2124.15."

---

## **Part 6: Applications and Takeaways**

### **Applications of Agents:**
- **Research:** Summarizing papers, identifying gaps.
- **Automation:** Booking flights, managing schedules.
- **Development:** Code generation and debugging.

### **Key Takeaways:**
1. **Agents = LLM + Tools:** Combining reasoning and acting.
2. **ReAct Framework:** The foundation of agentic systems, consisting of Thought, Action, and Observation.
3. **Future of Agents:** The agentic world will transform automation, reducing human effort in repetitive tasks.

---

## **References:**
- [Agents in LangChain](https://python.langchain.com/v0.1/doc)
- [LangChain Agents Tools](https://github.com/kyrolabs/awesome-l)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Code Link](https://colab.research.google.com/github/HandsOnLLM/Hands-On-Large-Language-Models/blob/main/chapter07/Chapter%207%20-%20Advanced%20Text%20Generation%20Techniques%20and%20Tools.ipynb#scrollTo=6tAr1962vS4T)

---

Start your journey with agents today and unleash their potential to automate your workflows! 🚀
