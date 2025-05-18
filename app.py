import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# Set up the page
st.set_page_config(page_title="Automation Decision Assistant", page_icon="🤖")
st.title("Grocery Distribution Automation Advisor")
st.markdown("""
Ask any question about the automation case study and get detailed analysis.
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Case study data
case_data = {
    "current_labor_cost": 12272000,
    "automated_labor_cost": 10257000,
    "automation_cost": 4000000,
    "annual_maintenance": 1000000,
    "shipments": 1000000,
    "stores": 50,
    "employee_data": {
        "receiving": {"count": 50, "wage": 12, "hours": 2000},
        "holding_picking": {"count": 250, "wage": 17, "hours": 10000},
        "shipping": {"count": 75, "wage": 14, "hours": 3000}
    }
}

# Calculate derived metrics
labor_savings = case_data['current_labor_cost'] - case_data['automated_labor_cost']
net_savings = labor_savings - case_data['annual_maintenance']
break_even = case_data['automation_cost'] / net_savings

# Response generation function
def generate_response(user_question):
    # Convert to lowercase for easier matching
    question = user_question.lower()
    
    # Basic question matching
    if any(word in question for word in ["hello", "hi", "greet"]):
        return "Hello! I can help you analyze the grocery distribution automation case study. Ask me about costs, savings, or whether to automate."
    
    elif any(word in question for word in ["cost", "spend", "expense"]):
        if "current" in question:
            return f"""
            **Current Annual Labor Costs:**
            - Receiving: 50 employees × $12/hr = ${50*40*52*12:,} per year
            - Holding & Picking: 250 employees × $17/hr = ${250*40*52*17:,} per year
            - Shipping: 75 employees × $14/hr = ${75*40*52*14:,} per year
            - **Total:** ${case_data['current_labor_cost']:,} per year
            """
        elif "automated" in question or "after" in question:
            return f"""
            **Labor Costs After Automation:**
            - Holding & Picking reduced to 131 employees (from 250)
            - Shipping increases to 150 employees (from 75)
            - Receiving remains at 50 employees
            - **Total:** ${case_data['automated_labor_cost']:,} per year
            - **Savings:** ${labor_savings:,} per year
            """
        else:
            return f"""
            **Cost Information:**
            - Current labor costs: ${case_data['current_labor_cost']:,}/year
            - Automated labor costs: ${case_data['automated_labor_cost']:,}/year
            - One-time automation cost: ${case_data['automation_cost']:,}
            - Annual maintenance: ${case_data['annual_maintenance']:,}
            """
    
    elif any(word in question for word in ["save", "saving", "benefit"]):
        return f"""
        **Savings Analysis:**
        - Labor cost reduction: ${labor_savings:,} per year
        - After maintenance costs: ${net_savings:,} net annual savings
        - Break-even in {break_even:.1f} years
        """
    
    elif any(word in question for word in ["break", "even", "payback"]):
        # Create break-even chart
        years = list(range(6))
        cumulative_costs = [case_data['automation_cost'] + year*case_data['annual_maintenance'] for year in years]
        cumulative_savings = [0] + [year*labor_savings for year in range(1,6)]
        
        fig, ax = plt.subplots()
        ax.plot(years, cumulative_costs, label="Total Automation Costs")
        ax.plot(years, cumulative_savings, label="Total Labor Savings")
        ax.axvline(x=break_even, color='red', linestyle='--', label=f'Break-even ({break_even:.1f} years)')
        ax.set_title("Break-even Analysis")
        ax.set_xlabel("Years")
        ax.set_ylabel("Dollars ($)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        
        return f"""
        **Break-even Calculation:**
        - One-time cost: ${case_data['automation_cost']:,}
        - Annual net savings: ${net_savings:,}
        - **Break-even point:** {break_even:.1f} years
        
        The chart shows cumulative costs and savings over time.
        """
    
    elif any(word in question for word in ["employee", "staff", "job", "worker"]):
        return f"""
        **Employee Impact:**
        - Current employees: 375 total
          - Receiving: 50
          - Holding & Picking: 250
          - Shipping: 75
        - After automation: 331 total
          - Receiving: 50 (no change)
          - Holding & Picking: 131 (-119)
          - Shipping: 150 (+75)
        - **Net reduction:** 44 employees
        """
    
    elif any(word in question for word in ["recommend", "should", "advise"]):
        return """
        **Recommendation:**
        
        *Arguments FOR Automation:*
        - Long-term cost savings (~$1M/year after year 4)
        - Improved operational efficiency
        - Competitive advantage through technology
        
        *Arguments AGAINST Automation:*
        - Significant upfront investment ($4M)
        - Workforce reduction (44 jobs)
        - Additional $1M/year maintenance costs
        
        *Consider:*
        - If the company has capital and prioritizes long-term savings → Automate
        - If workforce impact is a major concern → Delay automation
        """
    
    elif any(word in question for word in ["risk", "challenge", "problem"]):
        return """
        **Potential Risks:**
        1. Technology implementation risks
        2. Employee morale issues from layoffs
        3. Hidden maintenance costs
        4. Operational disruption during transition
        5. Technology becoming obsolete
        """
    
    elif any(word in question for word in ["data", "numbers", "statistics"]):
        # Create a data table
        df = pd.DataFrame({
            "Metric": [
                "Current Labor Cost", 
                "Automated Labor Cost",
                "Labor Savings",
                "One-time Automation Cost",
                "Annual Maintenance",
                "Net Annual Savings",
                "Break-even Period"
            ],
            "Value": [
                f"${case_data['current_labor_cost']:,}",
                f"${case_data['automated_labor_cost']:,}",
                f"${labor_savings:,}",
                f"${case_data['automation_cost']:,}",
                f"${case_data['annual_maintenance']:,}",
                f"${net_savings:,}",
                f"{break_even:.1f} years"
            ]
        })
        st.dataframe(df, hide_index=True)
        return "Here are the key numbers from the case study:"
    elif "how many" in question and "employee" in question:
        return """
        **Employee Impact Overview:**
        - **Before Automation:** 375 employees
        - **After Automation:** 331 employees
        - **Net Change:** -44 employees
        """

    elif "recover" in question or "recover cost" in question or "payback" in question:
        return f"""
        **Payback Period:**
        - With net savings of ${net_savings:,}/year
        - Automation cost: ${case_data['automation_cost']:,}
        - **Break-even in {break_even:.1f} years**
        """

    elif "shipping" in question and "change" in question:
        return """
        **Shipping Department Changes:**
        - Employees increase from 75 to 150
        - Possibly due to reallocation of automated processes
        - Suggests higher throughput or new responsibilities post-automation
        """

    elif "maintenance" in question:
        return f"""
        **Annual Maintenance:**
        - Recurring cost: ${case_data['annual_maintenance']:,} per year
        - Reduces gross savings but still yields **${net_savings:,}/year** in net benefits
        - Should be factored into long-term ROI analysis
        """

    elif "chart" in question and "savings" in question:
        years = list(range(6))
        cumulative_costs = [case_data['automation_cost'] + year * case_data['annual_maintenance'] for year in years]
        cumulative_savings = [0] + [year * labor_savings for year in range(1, 6)]

        fig, ax = plt.subplots()
        ax.plot(years, cumulative_costs, label="Cumulative Costs (Automation + Maintenance)")
        ax.plot(years, cumulative_savings, label="Cumulative Labor Savings")
        ax.axvline(x=break_even, color='red', linestyle='--', label=f"Break-even: {break_even:.1f} years")
        ax.set_xlabel("Years")
        ax.set_ylabel("USD ($)")
        ax.set_title("Cumulative Cost vs Savings")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        return f"Here's the cumulative cost vs. savings chart with a break-even point at {break_even:.1f} years."

    elif "assumption" in question:
        return """
        **Model Assumptions:**
        - Full automation implemented immediately
        - Labor savings are constant year-over-year
        - No additional operational disruptions or hidden costs
        - Annual hours: 2,080 per FTE assumed
        - Wage estimates are accurate and do not fluctuate
        """

    elif "shipment" in question and "%" in question:
        # Simulate new shipment load impact (just illustrative)
        new_shipments = case_data['shipments'] * 1.10
        cost_per_shipment = case_data['automated_labor_cost'] / case_data['shipments']
        new_cost = cost_per_shipment * new_shipments
        new_savings = case_data['current_labor_cost'] - new_cost
        return f"""
        **Impact of 10% Shipment Increase:**
        - New shipments: {int(new_shipments):,}
        - Estimated cost with automation: ${new_cost:,.0f}
        - New estimated savings: ${new_savings:,.0f}
        - Automation still leads to cost efficiency at larger volumes
        """

    elif "store" in question and "impact" in question:
        savings_per_store = net_savings / case_data['stores']
        return f"""
        **Per Store Impact:**
        - 50 stores total
        - Average savings per store: **${savings_per_store:,.0f}/year**
        - Automation supports scaling without linear labor cost increases
        """

    elif "long-term" in question or ("benefit" in question and "long" in question):
        return """
        **Long-Term Benefits:**
        - Significant operational savings
        - Enhanced productivity and throughput
        - Reduced dependency on manual labor
        - Competitive edge through technology integration
        - More scalable operations over time
        """

    elif "phase" in question or "phased" in question:
        return """
        **Phased Automation Possibility:**
        - A phased rollout can reduce initial risk and financial burden
        - Allows time for employee retraining and system adaptation
        - May delay full ROI but improve organizational readiness
        - Requires more granular planning and modular technology
        """

    
    else:
        return """
        I can help answer questions about:
        - Current vs automated labor costs
        - Break-even analysis
        - Employee impact
        - Whether to automate
        - Risks to consider
        
        Try asking something like:
        "What are the current labor costs?"
        "How much would we save with automation?"
        "Should we automate the distribution center?"
        """

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sidebar with quick facts
with st.sidebar:
    st.header("Quick Facts")
    st.metric("Current Labor Cost", f"${case_data['current_labor_cost']/1000000:.2f}M/year")
    st.metric("Automation Cost", f"${case_data['automation_cost']/1000000:.2f}M")
    st.metric("Annual Savings", f"${net_savings/1000000:.2f}M/year")
    st.metric("Break-even", f"{break_even:.1f} years")
    
    st.divider()
    st.header("Sample Questions")
    st.markdown("""
    - What are the current costs?
- How much would automation save?
- What's the employee impact?
- Should we automate?
- What are the risks?
- How many employees are affected by automation?
- How long will it take to recover the automation cost?
- What changes occur in the shipping department?
- What are the annual maintenance implications?
- Can you show a chart of savings vs costs?
- What are the assumptions behind these numbers?
- What if shipment volume increases by 10%?
- How does automation affect individual store performance?
- What are the long-term benefits of automation?
- Could this be phased instead of fully automated at once?
    """)

# Chat input
if prompt := st.chat_input("Ask about the automation case"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    response = generate_response(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})