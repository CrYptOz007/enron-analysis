# Enron Analysis
This is a business analysis report based on the Eron Database, which consists of approximately 500,000 internal emails that were made public following the collapse of the company in 2001. The analysis utilizes Python notebooks and various libraries including `sqlite3`, `pandas` and `matplotlib` to create a range of visualizations.

## Requirements
* Python 3.x
* Jupyter Notebook

## Usage
1. Open the `business_report.ipynb` notebook in Jupyter Notebook.

2. Run each cell in the notebook sequentially to generate the visualizations and perform the analysis.

## Visualizations
The report generates the following visualizations:

1. **Email Traffic Over Time:** Shows the trend of email traffic per month, providing insights into the volume and patterns of communication.

2. **Top Senders and Recipients:** Displays the top 10 senders and recipients of emails, highlighting the most active individuals or entities in the communication network.

3. **Email Distribution by Recipient Type:** Illustrates the distribution of emails based on recipient types, such as "To," "CC," and "BCC," offering insights into the email distribution patterns.

4. **Subject Keyword Analysis:** Analyzes the top 10 keywords in email subjects to identify frequently used terms, enabling a deeper understanding of the topics discussed.

5. **Internal vs. External Communication:** Compares the proportion of internal (within the organisation) and external (outside the organisation) communications, helping to gauge the extent of internal collaboration versus external interactions.

## Important Note
For the **Top Senders and Recipients** visualization, it's important to note that the calculation of email counts only considers individual email messages. It does not account for individual CCs, BCCs, or multiple recipients in the "To" field. Each email is treated as a single unit, regardless of the number of recipients involved.

## License
This program is licensed under the GNU 3.0 license. Please see the `LICENSE` file for more details.