import os
import re
import html
import yaml
import json
import argparse
import requests
import urllib.request
from bs4 import BeautifulSoup
import html2text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
WP_API_BASE = "https://public-api.wordpress.com/rest/v1.1/sites/terrytao.wordpress.com/posts"

def slugify(text, max_len=60):
    text = text.lower()
    text = re.sub(r'[\'\"’“”]', '', text)
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = text.strip('_')
    if len(text) > max_len:
        text = text[:max_len].rstrip('_')
    return text or "tao_post"

def clean_html_to_markdown(raw_html):
    if not raw_html:
        return ""
        
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # Preserve math in latex images or latex tags
    for img in soup.find_all('img'):
        alt = img.get('alt', '')
        classes = img.get('class', [])
        src = img.get('src', '')
        
        if 'latex' in classes or 'latex' in src or 'latex.php' in src:
            clean_math = alt.strip()
            if clean_math.startswith('$') and clean_math.endswith('$'):
                img.replace_with(clean_math)
            else:
                img.replace_with(f"${clean_math}$")
        elif alt:
            img.replace_with(f"[{alt}]")
            
    # Process custom latex markers like $latex ...$
    raw_str = str(soup)
    raw_str = re.sub(r'\$latex\s+(.+?)\$', r'$\1$', raw_str)
    
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0
    converter.protect_links = True
    converter.mark_code = True
    
    md_text = converter.handle(raw_str)
    
    # Clean excessive whitespace and decode remaining entities
    md_text = html.unescape(md_text)
    md_text = re.sub(r'\n{3,}', '\n\n', md_text).strip()
    return md_text

def fetch_wp_posts(count=20, page=1, category=None, search=None, tag=None):
    params = {
        'number': min(count, 100),
        'page': page
    }
    if category:
        params['category'] = category
    if search:
        params['search'] = search
    if tag:
        params['tag'] = tag
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; TerenceTaoDigitalTwin/1.0; +https://github.com/Paarthexe/twinterrytao)'
    }
    
    try:
        response = requests.get(WP_API_BASE, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        posts = data.get('posts', [])
        total_found = data.get('found', len(posts))
        return posts, total_found
    except Exception as e:
        print(f"Error fetching posts from WordPress API: {e}")
        return [], 0

def save_post_to_document(post, target_dir=DOCUMENTS_DIR, force=False):
    os.makedirs(target_dir, exist_ok=True)
    
    title = html.unescape(post.get('title', 'Untitled')).strip()
    # Strip HTML tags from title if any
    title = re.sub(r'<[^>]+>', '', title)
    
    url = post.get('URL', '')
    date_str = post.get('date', '')
    if date_str and len(date_str) >= 10:
        date_str = date_str[:10]
    else:
        date_str = ''
        
    categories_dict = post.get('categories', {})
    categories = list(categories_dict.keys()) if isinstance(categories_dict, dict) else []
    
    slug_base = post.get('slug') or slugify(title)
    filename = f"{slug_base}.md"
    filepath = os.path.join(target_dir, filename)
    
    raw_content = post.get('content', '')
    md_content = clean_html_to_markdown(raw_content)
    
    if not md_content:
        # Fallback to excerpt
        md_content = clean_html_to_markdown(post.get('excerpt', ''))
        
    frontmatter = {
        'title': title,
        'source': 'terrytao.wordpress.com',
        'url': url,
        'date': date_str,
        'categories': categories
    }
    
    yaml_header = yaml.dump(frontmatter, default_flow_style=None, sort_keys=False, allow_unicode=True).strip()
    full_doc = f"---\n{yaml_header}\n---\n\n{md_content}\n"
    
    status = "saved"
    if os.path.exists(filepath):
        if not force:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            if existing_content.strip() == full_doc.strip():
                return filepath, "skipped", title
            status = "updated"
        else:
            status = "overwritten"
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_doc)
        
    return filepath, status, title

def sync_tao_blog(count=None, all_posts=False, category=None, search=None, tag=None, target_dir=DOCUMENTS_DIR, force=False, verbose=True):
    os.makedirs(target_dir, exist_ok=True)
    
    fetch_all = all_posts or (count is None)
    remaining = count if not fetch_all else float('inf')
    page = 1
    total_saved = 0
    total_updated = 0
    total_skipped = 0
    processed_files = []
    
    if verbose:
        target_desc = "ALL posts (~1,000+ posts)" if fetch_all else f"{count} posts"
        print(f"[*] Starting blog sync from Terence Tao's WordPress blog (Target: {target_desc})...")
        if category:
            print(f"    Filtering by category: {category}")
        if search:
            print(f"    Filtering by search query: {search}")
            
    while remaining > 0:
        batch_size = 100 if fetch_all else min(int(remaining), 100)
        posts, total_found = fetch_wp_posts(count=batch_size, page=page, category=category, search=search, tag=tag)
        
        if not posts:
            if verbose and page == 1:
                print("[-] No posts returned from WordPress API.")
            break
            
        total_pages = (total_found + batch_size - 1) // batch_size if total_found > 0 else 1
        if verbose:
            print(f"[*] Processing page {page}/{total_pages} ({len(posts)} posts in batch, {total_found} total on blog)...")
            
        for post in posts:
            filepath, status, post_title = save_post_to_document(post, target_dir=target_dir, force=force)
            filename = os.path.basename(filepath)
            
            if status == "saved":
                total_saved += 1
            elif status in ("updated", "overwritten"):
                total_updated += 1
            elif status == "skipped":
                total_skipped += 1
                
            processed_files.append({
                "file": filename,
                "path": filepath,
                "title": post_title,
                "status": status,
                "url": post.get('URL', '')
            })
            
            if verbose and status != "skipped":
                print(f"    [{status.upper()}] {post_title} -> {filename}")
                
        if not fetch_all:
            remaining -= len(posts)
            
        if len(posts) < batch_size or (page * batch_size) >= total_found:
            break
        page += 1
        
    summary = {
        "total_fetched": len(processed_files),
        "saved": total_saved,
        "updated": total_updated,
        "skipped": total_skipped,
        "files": processed_files
    }
    
    if verbose:
        print(f"[+] Sync finished: {total_saved} saved, {total_updated} updated, {total_skipped} unchanged (Total processed: {len(processed_files)})")
        
    return summary

def extract_arxiv_ids_from_documents(directory=DOCUMENTS_DIR):
    """Scans local documents to extract cited arXiv identifiers."""
    arxiv_pattern = re.compile(
        r'arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v[0-9]+)?|[a-z\-]+/[0-9]{7}(?:v[0-9]+)?)|arXiv:([0-9]{4}\.[0-9]{4,5}(?:v[0-9]+)?|[a-z\-]+/[0-9]{7}(?:v[0-9]+)?)',
        re.IGNORECASE
    )
    found_ids = set()
    if not os.path.exists(directory):
        return []
        
    for filename in os.listdir(directory):
        if not filename.endswith('.md') or filename.startswith('arxiv_'):
            continue
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            matches = arxiv_pattern.findall(text)
            for m in matches:
                aid = m[0] or m[1]
                clean_id = re.sub(r'v[0-9]+$', '', aid.strip()).rstrip('.')
                if clean_id:
                    found_ids.add(clean_id)
        except Exception:
            pass
            
    return sorted(list(found_ids))

def fetch_arxiv_batch(arxiv_ids):
    """Queries public arXiv REST API for a batch of paper IDs."""
    import xml.etree.ElementTree as ET
    if not arxiv_ids:
        return []
        
    id_param = ",".join(arxiv_ids)
    url = f"http://export.arxiv.org/api/query?id_list={id_param}&max_results={len(arxiv_ids)}"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; TerenceTaoDigitalTwin/1.0; +https://github.com/Paarthexe/twinterrytao)'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            xml_data = resp.read().decode('utf-8')
            
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            id_elem = entry.find('atom:id', ns)
            if id_elem is None or not id_elem.text:
                continue
                
            raw_id = id_elem.text.strip().split('/abs/')[-1]
            clean_id = re.sub(r'v[0-9]+$', '', raw_id)
            
            title_elem = entry.find('atom:title', ns)
            title = " ".join(title_elem.text.strip().split()) if title_elem is not None and title_elem.text else f"arXiv:{clean_id}"
            
            summary_elem = entry.find('atom:summary', ns)
            summary = summary_elem.text.strip() if summary_elem is not None and summary_elem.text else ""
            
            published_elem = entry.find('atom:published', ns)
            date_str = published_elem.text[:10] if published_elem is not None and published_elem.text else ""
            
            authors = [a.find('atom:name', ns).text.strip() for a in entry.findall('atom:author', ns) if a.find('atom:name', ns) is not None]
            categories = ["research_paper", "arxiv"]
            for c in entry.findall('atom:category', ns):
                term = c.attrib.get('term')
                if term and term not in categories:
                    categories.append(term)
                    
            papers.append({
                "arxiv_id": clean_id,
                "title": title,
                "authors": authors,
                "summary": summary,
                "date": date_str,
                "categories": categories,
                "url": f"https://arxiv.org/abs/{clean_id}"
            })
        return papers
    except Exception as e:
        print(f"[-] Error querying arXiv API: {e}")
        return []

def sync_arxiv_papers(max_papers=50, target_dir=DOCUMENTS_DIR, force=False, verbose=True):
    """Discovers arXiv links in blog posts and saves official paper metadata and abstracts."""
    os.makedirs(target_dir, exist_ok=True)
    all_ids = extract_arxiv_ids_from_documents(target_dir)
    
    if verbose:
        print(f"[*] Discovered {len(all_ids)} unique arXiv paper references in blog documents.")
        
    to_fetch = []
    skipped_count = 0
    for aid in all_ids:
        safe_name = re.sub(r'[^a-zA-Z0-9_\.]', '_', aid)
        filename = f"arxiv_{safe_name}.md"
        filepath = os.path.join(target_dir, filename)
        if not force and os.path.exists(filepath):
            skipped_count += 1
        else:
            to_fetch.append(aid)
            
    if max_papers is not None:
        to_fetch = to_fetch[:max_papers]
        
    if verbose:
        print(f"[*] Ingesting {len(to_fetch)} new arXiv papers ({skipped_count} already saved)...")
        
    total_saved = 0
    processed_papers = []
    
    # Process in batches of 30
    batch_size = 30
    for i in range(0, len(to_fetch), batch_size):
        batch_ids = to_fetch[i:i+batch_size]
        papers = fetch_arxiv_batch(batch_ids)
        
        for p in papers:
            safe_name = re.sub(r'[^a-zA-Z0-9_\.]', '_', p['arxiv_id'])
            filename = f"arxiv_{safe_name}.md"
            filepath = os.path.join(target_dir, filename)
            
            authors_str = ", ".join(p['authors']) if p['authors'] else "Unknown"
            frontmatter = {
                'title': p['title'],
                'source': f"arXiv:{p['arxiv_id']}",
                'url': p['url'],
                'date': p['date'],
                'categories': p['categories'],
                'authors': p['authors']
            }
            yaml_header = yaml.dump(frontmatter, default_flow_style=None, sort_keys=False, allow_unicode=True).strip()
            
            doc_body = f"""---
{yaml_header}
---

# {p['title']}

**Authors**: {authors_str}  
**arXiv Identifier**: [{p['arxiv_id']}]({p['url']})  
**Primary Categories**: {', '.join(p['categories'])}  

## Abstract & Mathematical Overview

{p['summary']}
"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(doc_body)
                
            total_saved += 1
            processed_papers.append({
                "file": filename,
                "title": p['title'],
                "arxiv_id": p['arxiv_id'],
                "status": "saved"
            })
            if verbose:
                print(f"    [ARXIV SAVED] {p['title'][:60]}... ({p['arxiv_id']})")
                
    summary = {
        "total_discovered": len(all_ids),
        "total_saved": total_saved,
        "already_indexed": skipped_count,
        "papers": processed_papers
    }
    if verbose:
        print(f"[+] arXiv Ingestion complete: {total_saved} papers saved, {skipped_count} existing.")
    return summary

def list_local_documents(directory=DOCUMENTS_DIR):
    docs = []
    if not os.path.exists(directory):
        return docs
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(directory, filename)
        stat = os.stat(filepath)
        
        title = filename
        source = "terrytao.wordpress.com"
        url = ""
        date = ""
        categories = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read(2048) # Read frontmatter snippet
            if text.startswith('---'):
                parts = text.split('---', 2)
                if len(parts) >= 3:
                    meta = yaml.safe_load(parts[1])
                    if meta:
                        title = meta.get('title', title)
                        source = meta.get('source', source)
                        url = meta.get('url', url)
                        date = str(meta.get('date', ''))
                        categories = meta.get('categories', [])
        except Exception:
            pass
            
        docs.append({
            "filename": filename,
            "title": title,
            "source": source,
            "url": url,
            "date": date,
            "categories": categories,
            "size_bytes": stat.st_size,
            "modified_time": stat.st_mtime
        })
    return docs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape and synchronize Terence Tao blog posts & arXiv papers into markdown documents.")
    parser.add_argument('-a', '--all', action='store_true', default=False, help="Fetch all blog posts across entire blog archive")
    parser.add_argument('-n', '--count', type=int, default=None, help="Number of posts to fetch")
    parser.add_argument('-c', '--category', type=str, default=None, help="Filter posts by WordPress category (e.g. expository, math.CA)")
    parser.add_argument('-s', '--search', type=str, default=None, help="Search posts by keyword")
    parser.add_argument('-t', '--tag', type=str, default=None, help="Filter posts by tag")
    parser.add_argument('--arxiv', action='store_true', help="Discover and ingest arXiv papers cited in blog posts")
    parser.add_argument('--arxiv-count', type=int, default=50, help="Max arXiv papers to ingest (default: 50)")
    parser.add_argument('-f', '--force', action='store_true', help="Force overwrite existing documents")
    parser.add_argument('--list', action='store_true', help="List existing local markdown documents")
    
    args = parser.parse_args()
    
    if args.list:
        docs = list_local_documents()
        print(f"Found {len(docs)} local documents in {DOCUMENTS_DIR}:")
        for d in docs:
            print(f" - [{d['date'] or 'N/A'}] {d['title']} ({d['filename']})")
    elif args.arxiv:
        sync_arxiv_papers(max_papers=args.arxiv_count, force=args.force, verbose=True)
    else:
        sync_tao_blog(
            count=args.count,
            all_posts=(args.count is None or args.all),
            category=args.category,
            search=args.search,
            tag=args.tag,
            force=args.force,
            verbose=True
        )

