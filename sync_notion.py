"""
sync_notion.py — Pull data from Notion databases and generate Hugo data files + LaTeX CV.

Usage:
  1. Create a .env file with NOTION_API_KEY=your_secret_key
  2. Run: python sync_notion.py

This script queries each Notion database, transforms the data, and writes JSON
files to the Hugo `data/` directory. It also generates a LaTeX CV.
"""

import json
import os
import sys
from datetime import datetime

try:
    from notion_client import Client
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install notion-client python-dotenv")
    sys.exit(1)

load_dotenv()

# ===== Configuration =====
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if not NOTION_API_KEY:
    print("Error: NOTION_API_KEY not found in .env file")
    print("Create a .env file with: NOTION_API_KEY=your_secret_key")
    sys.exit(1)

# Database IDs (from your Notion workspace)
DB_IDS = {
    "publications": "b9c994a2ca314416bd4154ed3c0ed855",
    "news": "4ebaccdfb29f436e9597a4f82e6734e4",
    "team": "e0b51431da214dfebcdad7944eea1eee",
    "honors": "e54123bedbed48e2b3be4bbaeca29f39",
    "education": "b705910d828e43b6b40cc4a6135dd753",
    "projects": "3cbc15cf33644f44afe5efce27f2b2b4",
    "cv_only": "107046893bcc47a7b15d3fe1f403e831",
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

notion = Client(auth=NOTION_API_KEY)


def get_text(prop):
    """Extract plain text from a Notion rich_text or title property."""
    if not prop:
        return ""
    items = prop.get("rich_text") or prop.get("title") or []
    return "".join(item.get("plain_text", "") for item in items)


def get_number(prop):
    """Extract number from a Notion number property."""
    if not prop:
        return None
    return prop.get("number")


def get_select(prop):
    """Extract select value from a Notion select property."""
    if not prop:
        return ""
    sel = prop.get("select")
    return sel.get("name", "") if sel else ""


def get_checkbox(prop):
    """Extract checkbox value from a Notion checkbox property."""
    if not prop:
        return False
    return prop.get("checkbox", False)


def get_url(prop):
    """Extract URL from a Notion url property."""
    if not prop:
        return ""
    return prop.get("url", "") or ""


def get_date(prop):
    """Extract date string from a Notion date property."""
    if not prop:
        return ""
    date = prop.get("date")
    if not date:
        return ""
    return date.get("start", "")


def get_email(prop):
    """Extract email from a Notion email property."""
    if not prop:
        return ""
    return prop.get("email", "") or ""


def query_all(database_id):
    """Query all pages from a Notion database, handling pagination."""
    results = []
    has_more = True
    start_cursor = None

    while has_more:
        kwargs = {"database_id": database_id}
        if start_cursor:
            kwargs["start_cursor"] = start_cursor
        response = notion.databases.query(**kwargs)
        results.extend(response["results"])
        has_more = response.get("has_more", False)
        start_cursor = response.get("next_cursor")

    return results


def sync_publications():
    """Sync publications database."""
    pages = query_all(DB_IDS["publications"])
    pubs = []
    for page in pages:
        props = page["properties"]
        pubs.append({
            "Title": get_text(props.get("Title")),
            "Authors": get_text(props.get("Authors")),
            "Year": get_number(props.get("Year")),
            "Journal": get_select(props.get("Journal")),
            "Volume_Pages": get_text(props.get("Volume Pages")),
            "DOI": get_url(props.get("DOI")),
            "PDF_Link": get_url(props.get("PDF Link")),
            "Is_First_Author": get_checkbox(props.get("Is First Author")),
            "Featured_on_Cover": get_checkbox(props.get("Featured on Cover")),
            "Paper_Number": get_number(props.get("Paper Number")),
            "Category": get_select(props.get("Category")),
            "Notes": get_text(props.get("Notes")),
        })
    pubs.sort(key=lambda x: x.get("Paper_Number") or 0, reverse=True)
    return pubs


def sync_news():
    """Sync news & media database."""
    pages = query_all(DB_IDS["news"])
    items = []
    for page in pages:
        props = page["properties"]
        items.append({
            "Headline": get_text(props.get("Headline")),
            "Source": get_text(props.get("Source")),
            "Date": get_date(props.get("Date")),
            "URL": get_url(props.get("URL")),
            "Type": get_select(props.get("Type")),
            "Year": get_number(props.get("Year")),
        })
    items.sort(key=lambda x: x.get("Date") or "", reverse=True)
    return items


def sync_team():
    """Sync team members database."""
    pages = query_all(DB_IDS["team"])
    members = []
    for page in pages:
        props = page["properties"]
        members.append({
            "Name": get_text(props.get("Name")),
            "Role": get_select(props.get("Role")),
            "Bio": get_text(props.get("Bio")),
            "Start_Date": get_date(props.get("Start Date")),
            "End_Date": get_date(props.get("End Date")),
            "Status": get_select(props.get("Status")),
            "Email": get_email(props.get("Email")),
            "LinkedIn": get_url(props.get("LinkedIn")),
            "Google_Scholar": get_url(props.get("Google Scholar")),
            "Personal_Site": get_url(props.get("Personal Site")),
        })
    return members


def sync_honors():
    """Sync honors & awards database."""
    pages = query_all(DB_IDS["honors"])
    items = []
    for page in pages:
        props = page["properties"]
        date_str = get_date(props.get("Date"))
        # Format date as MM/YYYY
        display_date = ""
        if date_str:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                display_date = dt.strftime("%m/%Y")
            except ValueError:
                display_date = date_str
        items.append({
            "Award": get_text(props.get("Award")),
            "Date": display_date,
            "Date_raw": date_str,
            "Description": get_text(props.get("Description")),
        })
    items.sort(key=lambda x: x.get("Date_raw") or "", reverse=True)
    return items


def sync_education():
    """Sync education database."""
    pages = query_all(DB_IDS["education"])
    items = []
    for page in pages:
        props = page["properties"]
        items.append({
            "Degree": get_text(props.get("Degree")),
            "Institution": get_text(props.get("Institution")),
            "Years": get_text(props.get("Years")),
            "Advisor": get_text(props.get("Advisor")),
            "Order": get_number(props.get("Order")),
        })
    items.sort(key=lambda x: x.get("Order") or 0)
    return items


def parse_body(body_text):
    """Parse the Body field into structured subtopics.

    Format in Notion:
        First paragraph(s) = description (already in Description field)
        media: ... = media highlights line
        ### Title
        image: filename.png
        caption: ... (Journal Name Year, Vol, Pages)
        link: URL
    """
    if not body_text:
        return {"media_highlights": "", "subtopics": []}

    lines = body_text.split("\n")
    media_highlights = ""
    subtopics = []
    current = None

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("media:"):
            media_highlights = stripped[len("media:"):].strip()
        elif stripped.startswith("### "):
            if current:
                subtopics.append(current)
            current = {"title": stripped[4:].strip(), "image": "", "caption": "", "link": ""}
        elif stripped.startswith("image:") and current:
            current["image"] = stripped[len("image:"):].strip()
        elif stripped.startswith("caption:") and current:
            current["caption"] = stripped[len("caption:"):].strip()
        elif stripped.startswith("link:") and current:
            current["link"] = stripped[len("link:"):].strip()

    if current:
        subtopics.append(current)

    return {"media_highlights": media_highlights, "subtopics": subtopics}


def sync_projects():
    """Sync research projects database."""
    pages = query_all(DB_IDS["projects"])
    items = []
    for page in pages:
        props = page["properties"]
        body_text = get_text(props.get("Body"))
        parsed = parse_body(body_text)

        # Extract the intro paragraph from Body (everything before media: or ### )
        intro = ""
        if body_text:
            intro_lines = []
            for line in body_text.split("\n"):
                stripped = line.strip()
                if stripped.startswith("media:") or stripped.startswith("### "):
                    break
                if stripped:
                    intro_lines.append(stripped)
            intro = " ".join(intro_lines)

        items.append({
            "Project": get_text(props.get("Project")),
            "Description": get_text(props.get("Description")),
            "Category": get_select(props.get("Category")),
            "Order": get_number(props.get("Order")),
            "Slug": get_text(props.get("Slug")),
            "Hero_Image": get_text(props.get("Hero_Image")),
            "Full_Description": intro,
            "Media_Highlights": parsed["media_highlights"],
            "Subtopics": parsed["subtopics"],
        })
    items.sort(key=lambda x: x.get("Order") or 0)
    return items


def sync_cv_only():
    """Sync CV-only sections database (Research Experience, Teaching, etc.)."""
    pages = query_all(DB_IDS["cv_only"])
    items = []
    for page in pages:
        props = page["properties"]
        items.append({
            "Name": get_text(props.get("Name")),
            "Section": get_select(props.get("Section")),
            "Content": get_text(props.get("Content")),
            "Order": get_number(props.get("Order")),
        })
    items.sort(key=lambda x: x.get("Order") or 0)
    return items


def write_json(data, filename):
    """Write data to a JSON file in the data directory."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {len(data)} items to {filename}")


def generate_latex_cv(pubs, honors, education, cv_only=None):
    """Generate a LaTeX CV from the synced data."""
    cv_dir = os.path.join(os.path.dirname(__file__), "cv")
    os.makedirs(cv_dir, exist_ok=True)

    selected = [p for p in pubs if p["Category"] == "Selected"]
    selected.sort(key=lambda x: x.get("Paper_Number") or 0, reverse=True)
    other = [p for p in pubs if p["Category"] != "Selected"]
    other.sort(key=lambda x: x.get("Paper_Number") or 0, reverse=True)

    def escape_latex(text):
        """Escape special LaTeX characters."""
        if not text:
            return ""
        replacements = {
            "&": r"\&",
            "%": r"\%",
            "#": r"\#",
            "_": r"\_",
            "~": r"\textasciitilde{}",
            "α": r"$\alpha$",
            "β": r"$\beta$",
            "γ": r"$\gamma$",
            "δ": r"$\delta$",
            "μ": r"$\mu$",
            "†": r"$\dagger$",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def format_pub_latex(pub):
        authors = escape_latex(pub["Authors"])
        title = escape_latex(pub["Title"])
        journal = escape_latex(pub["Journal"])
        vol = escape_latex(pub["Volume_Pages"])
        year = pub["Year"]
        # Bold "Min, J." in author list
        authors = authors.replace("Min, J.", r"\textbf{Min, J.}")
        entry = f"{authors} ({year}). {title}. \\textit{{{journal}}}"
        if vol:
            entry += f", {vol}"
        entry += "."
        if pub.get("Notes"):
            entry += f" {escape_latex(pub['Notes'])}"
        return entry

    lines = []
    lines.append(r"\documentclass[11pt,a4paper]{article}")
    lines.append(r"\usepackage[margin=1in]{geometry}")
    lines.append(r"\usepackage{enumitem}")
    lines.append(r"\usepackage{hyperref}")
    lines.append(r"\usepackage[T1]{fontenc}")
    lines.append(r"\usepackage{charter}")
    lines.append(r"\usepackage{titlesec}")
    lines.append(r"\titleformat{\section}{\large\bfseries}{}{0em}{}[\titlerule]")
    lines.append(r"\titlespacing{\section}{0pt}{12pt}{6pt}")
    lines.append(r"\setlength{\parindent}{0pt}")
    lines.append(r"\begin{document}")
    lines.append("")
    lines.append(r"{\LARGE \textbf{Jihong Min}} \\[6pt]")
    lines.append(r"Presidential Young Professor, Department of Biomedical Engineering \\")
    lines.append(r"National University of Singapore \\")
    lines.append(r"Email: jihong.min@nus.edu.sg \\")
    lines.append(r"\href{https://scholar.google.com/citations?user=T4pVa1UAAAAJ}{Google Scholar}")
    lines.append("")

    # Education
    lines.append(r"\section{Education}")
    for edu in education:
        lines.append(f"\\textbf{{{escape_latex(edu['Years'])}}} \\hfill {escape_latex(edu['Degree'])} \\\\")
        lines.append(f"{escape_latex(edu['Institution'])}")
        if edu.get("Advisor"):
            lines.append(f" \\\\ \\textit{{Advisor: {escape_latex(edu['Advisor'])}}}")
        lines.append("\\\\[6pt]")
    lines.append("")

    # CV-only sections: Research Experience
    if cv_only:
        # Section name mapping for LaTeX
        section_map = {
            "Research Experience": "Research \\& Work Experience",
            "Teaching & Mentoring": "Teaching and Mentoring",
            "Conferences & Talks": "Conference Presentations, Poster Sessions, Invited Talks, and Workshops",
            "Academic Service": "Academic Service",
            "Proposal Writing": "Proposal Writing Experience",
            "Patents": "Patents",
        }
        # Sections to include before Honors (Research Experience only)
        for item in cv_only:
            if item["Section"] == "Research Experience":
                latex_title = section_map.get(item["Section"], item["Section"])
                lines.append(f"\\section{{{latex_title}}}")
                for content_line in item["Content"].split("\n"):
                    content_line = content_line.strip()
                    if not content_line:
                        lines.append("\\\\[6pt]")
                    elif content_line.startswith("- "):
                        lines.append(f"\\quad {escape_latex(content_line[2:])}")
                        lines.append("\\\\")
                    elif "|" in content_line:
                        parts = content_line.split("|", 1)
                        lines.append(f"\\textbf{{{escape_latex(parts[0].strip())}}} \\hfill {escape_latex(parts[1].strip())} \\\\")
                    else:
                        lines.append(f"{escape_latex(content_line)} \\\\")
                lines.append("")

    # Honors
    lines.append(r"\section{Honors \& Awards}")
    lines.append(r"\begin{itemize}[leftmargin=*, nosep]")
    for honor in honors:
        lines.append(f"  \\item {escape_latex(honor['Date'])}. {escape_latex(honor['Award'])}")
    lines.append(r"\end{itemize}")
    lines.append("")

    # Selected Publications
    total = len(pubs)
    first_author_count = len([p for p in pubs if p["Is_First_Author"]])
    lines.append(r"\section{Selected Publications}")
    lines.append(f"({total} papers with {first_author_count} as first/co-first author, "
                 f"$>$7000 citations, h-index 23, updated {datetime.now().strftime('%m/%Y')})")
    lines.append("")
    lines.append(r"\begin{enumerate}[leftmargin=*, nosep]")
    for pub in selected:
        lines.append(f"  \\item {format_pub_latex(pub)}")
    lines.append(r"\end{enumerate}")
    lines.append("")

    # Other Publications
    lines.append(r"\section{Other Publications}")
    lines.append(r"\begin{enumerate}[leftmargin=*, nosep]")
    for pub in other:
        lines.append(f"  \\item {format_pub_latex(pub)}")
    lines.append(r"\end{enumerate}")
    lines.append("")

    # CV-only sections after publications
    if cv_only:
        section_map = {
            "Research Experience": "Research \\& Work Experience",
            "Teaching & Mentoring": "Teaching and Mentoring",
            "Conferences & Talks": "Conference Presentations, Poster Sessions, Invited Talks, and Workshops",
            "Academic Service": "Academic Service",
            "Proposal Writing": "Proposal Writing Experience",
            "Patents": "Patents",
        }
        for item in cv_only:
            if item["Section"] == "Research Experience":
                continue  # Already added before Honors
            latex_title = section_map.get(item["Section"], item["Name"])
            lines.append(f"\\section{{{latex_title}}}")
            in_list = False
            content_lines = item["Content"].split("\n")
            for content_line in content_lines:
                content_line = content_line.strip()
                if content_line.startswith("- "):
                    if not in_list:
                        lines.append(r"\begin{itemize}[leftmargin=*, nosep]")
                        in_list = True
                    lines.append(f"  \\item {escape_latex(content_line[2:])}")
                else:
                    if in_list:
                        lines.append(r"\end{itemize}")
                        in_list = False
                    if not content_line:
                        lines.append("\\vspace{4pt}")
                    else:
                        lines.append(f"{escape_latex(content_line)} \\\\")
            if in_list:
                lines.append(r"\end{itemize}")
            lines.append("")

    lines.append(r"\end{document}")

    tex_path = os.path.join(cv_dir, "jihong_min_cv.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Generated LaTeX CV: {tex_path}")
    print("  To compile: cd cv && pdflatex jihong_min_cv.tex")


def main():
    print("Syncing Notion databases to Hugo data files...")
    print()

    print("[1/7] Publications...")
    pubs = sync_publications()
    write_json(pubs, "publications.json")

    print("[2/7] News & Media...")
    news = sync_news()
    write_json(news, "news.json")

    print("[3/7] Team Members...")
    team = sync_team()
    write_json(team, "team.json")

    print("[4/7] Honors & Awards...")
    honors = sync_honors()
    write_json(honors, "honors.json")

    print("[5/7] Education...")
    education = sync_education()
    write_json(education, "education.json")

    print("[6/7] Research Projects...")
    projects = sync_projects()
    write_json(projects, "projects.json")

    print("[7/7] CV-Only Sections...")
    cv_only = sync_cv_only()
    write_json(cv_only, "cv_only.json")

    print()
    print("Generating LaTeX CV...")
    generate_latex_cv(pubs, honors, education, cv_only)

    print()
    print("Done! Now run: hugo server")


if __name__ == "__main__":
    main()
