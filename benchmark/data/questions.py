from __future__ import annotations

import json

from benchmark.paths import QUESTIONS_JSON, ensure_dirs

QUESTIONS = [
    {"id": "q001", "category": "character", "question": "Why is Mrs. Bennet eager for Mr. Bingley to visit Longbourn?"},
    {"id": "q002", "category": "character", "question": "How does Mr. Darcy describe Elizabeth Bennet at the first assembly?"},
    {"id": "q003", "category": "plot", "question": "Why does Jane Bennet stay at Netherfield after visiting Caroline Bingley?"},
    {"id": "q004", "category": "relationship", "question": "What causes Elizabeth Bennet to dislike Mr. Darcy early in the novel?"},
    {"id": "q005", "category": "character", "question": "What role does Mr. Collins hope to play in the Bennet family?"},
    {"id": "q006", "category": "plot", "question": "Why does Mr. Collins propose to Elizabeth Bennet?"},
    {"id": "q007", "category": "plot", "question": "How does Elizabeth respond to Mr. Collins's proposal?"},
    {"id": "q008", "category": "relationship", "question": "Why does Charlotte Lucas accept Mr. Collins's proposal?"},
    {"id": "q009", "category": "character", "question": "What does Mr. Wickham tell Elizabeth about Mr. Darcy?"},
    {"id": "q010", "category": "plot", "question": "Why does the Netherfield party leave Hertfordshire?"},
    {"id": "q011", "category": "relationship", "question": "How does Jane react when Mr. Bingley leaves for London?"},
    {"id": "q012", "category": "setting", "question": "Where does Elizabeth visit Charlotte after Charlotte's marriage?"},
    {"id": "q013", "category": "character", "question": "How is Lady Catherine de Bourgh connected to Mr. Darcy?"},
    {"id": "q014", "category": "plot", "question": "What happens when Darcy first proposes to Elizabeth at Hunsford?"},
    {"id": "q015", "category": "character", "question": "What accusations does Elizabeth make against Darcy during his first proposal?"},
    {"id": "q016", "category": "plot", "question": "What important information does Darcy reveal in his letter to Elizabeth?"},
    {"id": "q017", "category": "relationship", "question": "How does Darcy explain his interference in Jane and Bingley's relationship?"},
    {"id": "q018", "category": "character", "question": "What does Darcy's letter reveal about Wickham's conduct toward Georgiana Darcy?"},
    {"id": "q019", "category": "theme", "question": "How does Elizabeth's opinion of Darcy begin to change after reading his letter?"},
    {"id": "q020", "category": "setting", "question": "Why does Elizabeth visit Pemberley with the Gardiners?"},
    {"id": "q021", "category": "character", "question": "How does the housekeeper at Pemberley describe Mr. Darcy?"},
    {"id": "q022", "category": "relationship", "question": "How does Darcy behave when Elizabeth unexpectedly meets him at Pemberley?"},
    {"id": "q023", "category": "character", "question": "What impression does Georgiana Darcy make on Elizabeth?"},
    {"id": "q024", "category": "plot", "question": "What news about Lydia interrupts Elizabeth's visit in Derbyshire?"},
    {"id": "q025", "category": "plot", "question": "With whom does Lydia Bennet run away?"},
    {"id": "q026", "category": "family", "question": "Why does Lydia's elopement threaten the Bennet family's reputation?"},
    {"id": "q027", "category": "plot", "question": "Who helps arrange Lydia and Wickham's marriage?"},
    {"id": "q028", "category": "character", "question": "Why does Darcy keep his role in Lydia's marriage quiet?"},
    {"id": "q029", "category": "relationship", "question": "How does Elizabeth learn about Darcy's help with Lydia's marriage?"},
    {"id": "q030", "category": "plot", "question": "What happens when Mr. Bingley returns to Netherfield?"},
    {"id": "q031", "category": "relationship", "question": "How does Jane respond to Bingley's renewed attention?"},
    {"id": "q032", "category": "plot", "question": "Why does Lady Catherine visit Elizabeth at Longbourn near the end of the novel?"},
    {"id": "q033", "category": "relationship", "question": "What demand does Lady Catherine make of Elizabeth?"},
    {"id": "q034", "category": "character", "question": "How does Elizabeth respond to Lady Catherine's attempt to control her?"},
    {"id": "q035", "category": "relationship", "question": "How does Lady Catherine's visit affect Darcy's hopes?"},
    {"id": "q036", "category": "plot", "question": "How does Darcy propose to Elizabeth a second time?"},
    {"id": "q037", "category": "relationship", "question": "Why does Elizabeth accept Darcy's second proposal?"},
    {"id": "q038", "category": "character", "question": "How does Mr. Bennet react when Elizabeth tells him she will marry Darcy?"},
    {"id": "q039", "category": "character", "question": "How does Mrs. Bennet react to Elizabeth's engagement to Darcy?"},
    {"id": "q040", "category": "theme", "question": "How does the novel contrast first impressions with deeper knowledge?"},
    {"id": "q041", "category": "theme", "question": "What examples of pride appear in Darcy's behavior?"},
    {"id": "q042", "category": "theme", "question": "What examples of prejudice appear in Elizabeth's judgment?"},
    {"id": "q043", "category": "family", "question": "How does Mr. Bennet's parenting contribute to Lydia's behavior?"},
    {"id": "q044", "category": "character", "question": "How is Mary Bennet different from her sisters?"},
    {"id": "q045", "category": "character", "question": "What role does Caroline Bingley play in Darcy and Elizabeth's relationship?"},
    {"id": "q046", "category": "setting", "question": "What is significant about Rosings Park in the story?"},
    {"id": "q047", "category": "setting", "question": "What does Pemberley reveal about Darcy's character?"},
    {"id": "q048", "category": "relationship", "question": "How do the Gardiners influence Elizabeth's understanding of Darcy?"},
    {"id": "q049", "category": "plot", "question": "What marriages conclude Pride and Prejudice?"},
    {"id": "q050", "category": "theme", "question": "How does marriage function as both romance and economic security in the novel?"},
]


def write_questions(force: bool = False) -> None:
    ensure_dirs()
    if QUESTIONS_JSON.exists() and not force:
        return
    QUESTIONS_JSON.write_text(json.dumps(QUESTIONS, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

