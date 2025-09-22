def generator(input_text, contexts):
    """
    The generator combines the best contexts and inputs into a short section.
    """
    if not contexts:
        return f"""
            <p><b>Input text:</b> {input_text}</p>
            <p><b>Warning:</b> No matching context in the knowledge base.</p>
        """

    snippets = []
    for doc in contexts:
        snippet_text = doc.text.strip()[:800]
        snippets.append(f"<b> - Source ({doc.id}):</b> {snippet_text}")

    context_html = "<br>".join(snippets)
    input_text = input_text.strip()

    html_msg = f"""
        <p>The following section was prepared based on available materials and the company description.</p>
        <h3>Context</h3>
        <p>{context_html}</p>
        <h3>Input</h3>
        <p>{input_text}</p>
    """

    return html_msg
