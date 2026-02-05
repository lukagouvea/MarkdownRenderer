"""
Componente Tkinter para Renderização de Markdown
Usa tk.Text com tags customizadas para melhor controle e renderização
"""

import tkinter as tk
import tkinter.font as tkfont
import customtkinter as ctk
import re


class MarkdownText(ctk.CTkTextbox):
    """Widget Text com suporte nativo a Markdown"""
    
    def __init__(self, master, **kwargs):
        # Configurações padrão
        defaults = {
            'wrap': 'word',
            'padx': 15,
            'pady': 15,
            'fg_color': '#ffffff',
            'text_color': '#333333',
            'font': ('Segoe UI', 11),
            'spacing1': 2,
            'spacing2': 2,
            'spacing3': 5,
            'state': 'disabled',
            'cursor': 'arrow',
            'corner_radius': 0,
            'border_width': 0,
            'activate_scrollbars': True
        }
        
        if 'bg' in kwargs: kwargs['fg_color'] = kwargs.pop('bg')
        if 'fg' in kwargs: kwargs['text_color'] = kwargs.pop('fg')
        if 'borderwidth' in kwargs: kwargs['border_width'] = kwargs.pop('borderwidth')
        if 'relief' in kwargs: kwargs.pop('relief')
        if 'yscrollcommand' in kwargs: kwargs.pop('yscrollcommand')

        defaults.update(kwargs)
        super().__init__(master, **defaults)
        
        self._setup_tags()
    
    def _setup_tags(self):
        """Configura as tags de formatação"""
        # Fontes
        base_font = tkfont.Font(font=self._textbox.cget('font'))
        base_size = int(base_font.cget('size'))+3
        base_family = base_font.cget('family')
        
        # Cabeçalhos
        self._textbox.tag_config('h1', font=('Segoe UI', base_size + 12, 'bold'), 
                          foreground='#1a1a2e', spacing1=20, spacing3=10)
        self._textbox.tag_config('h2', font=('Segoe UI', base_size + 8, 'bold'), 
                          foreground='#16213e', spacing1=18, spacing3=8)
        self._textbox.tag_config('h3', font=('Segoe UI', base_size + 5, 'bold'), 
                          foreground='#1f4068', spacing1=15, spacing3=6)
        self._textbox.tag_config('h4', font=('Segoe UI', base_size + 3, 'bold'), 
                          foreground='#1b1b2f', spacing1=12, spacing3=5)
        self._textbox.tag_config('h5', font=('Segoe UI', base_size + 2, 'bold'), 
                          foreground='#464866', spacing1=10, spacing3=4)
        self._textbox.tag_config('h6', font=('Segoe UI', base_size + 1, 'bold'), 
                          foreground='#6b778d', spacing1=8, spacing3=3)
        
        # Formatação de texto
        self._textbox.tag_config('bold', font=(base_family, base_size, 'bold'))
        self._textbox.tag_config('italic', font=(base_family, base_size, 'italic'))
        self._textbox.tag_config('bold_italic', font=(base_family, base_size, 'bold italic'))
        self._textbox.tag_config('strikethrough', overstrike=True, foreground='#888888')
        self._textbox.tag_config('underline', underline=True)
        
        # Código inline
        self._textbox.tag_config('code_inline', 
                  font=('Consolas', base_size), 
                          background='#f0f0f0',
                          foreground='#d63384',
                          spacing1=2)
        
        # Bloco de código
        self._textbox.tag_config('code_block', 
                  font=('Consolas', base_size),
                          background='#1e1e1e',
                          foreground='#d4d4d4',
                          spacing1=10,
                          spacing3=10,
                          lmargin1=20,
                          lmargin2=20,
                          rmargin=20)
        
        # Syntax highlighting para código
        self._textbox.tag_config('code_keyword', foreground='#569cd6', font=('Consolas', base_size - 1))
        self._textbox.tag_config('code_string', foreground='#ce9178', font=('Consolas', base_size - 1))
        self._textbox.tag_config('code_comment', foreground='#6a9955', font=('Consolas', base_size - 1))
        self._textbox.tag_config('code_number', foreground='#b5cea8', font=('Consolas', base_size - 1))
        self._textbox.tag_config('code_function', foreground='#dcdcaa', font=('Consolas', base_size - 1))
        self._textbox.tag_config('code_class', foreground='#4ec9b0', font=('Consolas', base_size - 1))
        self._textbox.tag_config('code_decorator', foreground='#c586c0', font=('Consolas', base_size - 1))
        self._textbox.tag_config('code_operator', foreground='#d4d4d4', font=('Consolas', base_size - 1))
        
        # Citação
        self._textbox.tag_config('blockquote', 
                          font=('Segoe UI', base_size, 'italic'),
                          foreground='#6c757d',
                          background='#f8f9fa',
                          lmargin1=30,
                          lmargin2=30,
                          spacing1=8,
                          spacing3=8,
                          borderwidth=3)
        
        # Links
        self._textbox.tag_config('link', foreground='#0d6efd', underline=True)
        self._textbox.tag_bind('link', '<Enter>', lambda e: self.configure(cursor='hand2'))
        self._textbox.tag_bind('link', '<Leave>', lambda e: self.configure(cursor='arrow'))
        
        # Listas
        self._textbox.tag_config('list_item', lmargin1=25, lmargin2=40)
        self._textbox.tag_config('list_bullet', foreground='#6c757d')
        self._textbox.tag_config('list_number', foreground='#0d6efd', font=('Segoe UI', base_size, 'bold'))
        
        # Linha horizontal
        self._textbox.tag_config('hr', font=('Segoe UI', 4), foreground='#dee2e6', 
                          spacing1=15, spacing3=15, justify='center')
        
        # Tabela
        self._textbox.tag_config('table_border', font=('Consolas', base_size),
                          foreground='#6c757d')
        self._textbox.tag_config('table_header', font=('Consolas', base_size, 'bold'),
                          background='#e9ecef', foreground='#212529')
        self._textbox.tag_config('table_cell', font=('Consolas', base_size),
                          background='#ffffff')
        self._textbox.tag_config('table_row_alt', font=('Consolas', base_size),
                          background='#f8f9fa')
        
        # Checkbox
        self._textbox.tag_config('checkbox_done', foreground='#198754')
        self._textbox.tag_config('checkbox_pending', foreground='#dc3545')


class MarkdownRenderer(MarkdownText):
    """Widget CTkTextbox com renderização de Markdown"""
    
    # Palavras-chave para syntax highlighting
    PYTHON_KEYWORDS = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
        'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
        'while', 'with', 'yield', 'print', 'len', 'range', 'str', 'int',
        'float', 'list', 'dict', 'set', 'tuple', 'open', 'input', 'type'
    }
    
    JS_KEYWORDS = {
        'async', 'await', 'break', 'case', 'catch', 'class', 'const', 'continue',
        'debugger', 'default', 'delete', 'do', 'else', 'export', 'extends',
        'finally', 'for', 'function', 'if', 'import', 'in', 'instanceof',
        'let', 'new', 'return', 'static', 'super', 'switch', 'this', 'throw',
        'try', 'typeof', 'var', 'void', 'while', 'with', 'yield', 'console',
        'log', 'true', 'false', 'null', 'undefined'
    }
    
    def __init__(self, master, markdown_text="", **kwargs):
        super().__init__(master, **kwargs)
        self._render_markdown(markdown_text)
    
    def set_markdown(self, markdown_text: str):
        """Define o texto Markdown a ser renderizado"""
        self._render_markdown(markdown_text)
    
    def _render_markdown(self, text: str):
        """Processa e renderiza o Markdown"""
        self.configure(state='normal')
        self.delete("0.0", "end")
        
        lines = text.split('\n')
        i = 0
        in_code_block = False
        code_block_content = []
        code_language = ""
        
        while i < len(lines):
            line = lines[i]
            
            # Bloco de código
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_language = line.strip()[3:].strip().lower()
                    code_block_content = []
                else:
                    in_code_block = False
                    self._insert_code_block('\n'.join(code_block_content), code_language)
                    code_block_content = []
                    code_language = ""
                i += 1
                continue
            
            if in_code_block:
                code_block_content.append(line)
                i += 1
                continue
            
            # Linha horizontal
            if re.match(r'^(-{3,}|\*{3,}|_{3,})\s*$', line.strip()):
                self.insert(tk.END, '─' * 60 + '\n', 'hr')
                i += 1
                continue
            
            # Cabeçalhos
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                level = len(header_match.group(1))
                content = header_match.group(2)
                self._insert_formatted_text(content, f'h{level}')
                self.insert(tk.END, '\n')
                i += 1
                continue
            
            # Citação
            if line.strip().startswith('>'):
                quote_lines = []
                while i < len(lines) and lines[i].strip().startswith('>'):
                    quote_lines.append(lines[i].strip()[1:].strip())
                    i += 1
                quote_text = ' '.join(quote_lines)
                self.insert(tk.END, '┃ ', 'blockquote')
                self._insert_formatted_text(quote_text, 'blockquote')
                self.insert(tk.END, '\n\n')
                continue
            
            # Lista não ordenada
            list_match = re.match(r'^(\s*)([-*+])\s+(.+)$', line)
            if list_match:
                indent = len(list_match.group(1)) // 2
                content = list_match.group(3)
                
                # Checkbox
                checkbox_match = re.match(r'\[([ xX])\]\s*(.+)', content)
                if checkbox_match:
                    checked = checkbox_match.group(1).lower() == 'x'
                    text_content = checkbox_match.group(2)
                    checkbox = '☑' if checked else '☐'
                    tag = 'checkbox_done' if checked else 'checkbox_pending'
                    self.insert(tk.END, '  ' * indent + checkbox + ' ', tag)
                    self._insert_formatted_text(text_content, 'list_item')
                else:
                    self.insert(tk.END, '  ' * indent + '• ', 'list_bullet')
                    self._insert_formatted_text(content, 'list_item')
                
                self.insert(tk.END, '\n')
                i += 1
                continue
            
            # Lista ordenada
            ordered_match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', line)
            if ordered_match:
                indent = len(ordered_match.group(1)) // 2
                num = ordered_match.group(2)
                content = ordered_match.group(3)
                self.insert(tk.END, '  ' * indent + f'{num}. ', 'list_number')
                self._insert_formatted_text(content, 'list_item')
                self.insert(tk.END, '\n')
                i += 1
                continue
            
            # Tabela
            if '|' in line and i + 1 < len(lines) and re.match(r'^[\s|:-]+$', lines[i + 1]):
                table_lines = []
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                self._insert_table(table_lines)
                continue
            
            # Parágrafo normal
            if line.strip():
                self._insert_formatted_text(line)
                self.insert(tk.END, '\n')
            else:
                self.insert(tk.END, '\n')
            
            i += 1

        self.configure(state='disabled')
    
    def _insert_formatted_text(self, text: str, base_tag: str = None):
        """Insere texto com formatação inline"""
        pattern = re.compile(
            r'(?P<bold_italic>\*\*\*(?P<bold_italic_text>.+?)\*\*\*|___(?P<bold_italic_text2>.+?)___)'
            r'|(?P<bold>\*\*(?P<bold_text>.+?)\*\*|__(?P<bold_text2>.+?)__)'
            r'|(?P<italic>\*(?P<italic_text>.+?)\*|_(?P<italic_text2>.+?)_)'
            r'|(?P<strike>~~(?P<strike_text>.+?)~~)'
            r'|(?P<code>`(?P<code_text>[^`]+)`)' 
            r'|(?P<link>\[(?P<link_text>[^\]]+)\]\((?P<link_url>[^)]+)\))'
        )

        last_end = 0
        for match in pattern.finditer(text):
            start, end = match.span()
            # Texto antes da formatação
            if start > last_end:
                plain_text = text[last_end:start]
                if base_tag:
                    self.insert(tk.END, plain_text, base_tag)
                else:
                    self.insert(tk.END, plain_text)

            if match.group('bold_italic'):
                content = match.group('bold_italic_text') or match.group('bold_italic_text2')
                tags = ('bold_italic', base_tag) if base_tag else ('bold_italic',)
                self.insert(tk.END, content, tags)
            elif match.group('bold'):
                content = match.group('bold_text') or match.group('bold_text2')
                tags = ('bold', base_tag) if base_tag else ('bold',)
                self.insert(tk.END, content, tags)
            elif match.group('italic'):
                content = match.group('italic_text') or match.group('italic_text2')
                tags = ('italic', base_tag) if base_tag else ('italic',)
                self.insert(tk.END, content, tags)
            elif match.group('strike'):
                content = match.group('strike_text')
                tags = ('strikethrough', base_tag) if base_tag else ('strikethrough',)
                self.insert(tk.END, content, tags)
            elif match.group('code'):
                content = match.group('code_text')
                tags = ('code_inline', base_tag) if base_tag else ('code_inline',)
                self.insert(tk.END, content, tags)
            elif match.group('link'):
                link_text = match.group('link_text')
                # link_url = match.group('link_url')  # Pode ser usado para abrir links
                tags = ('link', base_tag) if base_tag else ('link',)
                self.insert(tk.END, link_text, tags)

            last_end = end
        
        # Texto restante
        if last_end < len(text):
            remaining = text[last_end:]
            if base_tag:
                self.insert(tk.END, remaining, base_tag)
            else:
                self.insert(tk.END, remaining)
    
    def _insert_code_block(self, code: str, language: str):
        """Insere bloco de código com syntax highlighting"""
        self.insert(tk.END, '\n')
        
        # Cabeçalho do bloco de código
        if language:
            lang_display = language.upper()
            self.insert(tk.END, f' {lang_display} \n', 'code_block')
        
        # Aplicar syntax highlighting
        if language in ('python', 'py'):
            self._highlight_python(code)
        elif language in ('javascript', 'js', 'typescript', 'ts'):
            self._highlight_javascript(code)
        else:
            self.insert(tk.END, code + '\n', 'code_block')

        self.insert(tk.END, '\n')
    
    def _highlight_python(self, code: str):
        """Syntax highlighting para Python"""
        # Padrões para Python
        patterns = [
            (r'#.*$', 'code_comment'),                           # Comentários
            (r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')', 'code_string'),  # Docstrings
            (r'(["\'])(?:(?!\1|\\).|\\.)*\1', 'code_string'),    # Strings
            (r'\b(\d+\.?\d*)\b', 'code_number'),                 # Números
            (r'@\w+', 'code_decorator'),                          # Decoradores
            (r'\bdef\s+(\w+)', 'code_function'),                 # Funções
            (r'\bclass\s+(\w+)', 'code_class'),                  # Classes
        ]
        
        lines = code.split('\n')
        for line in lines:
            self._highlight_line(line, patterns, self.PYTHON_KEYWORDS)
            self.insert(tk.END, '\n', 'code_block')
    
    def _highlight_javascript(self, code: str):
        """Syntax highlighting para JavaScript"""
        patterns = [
            (r'//.*$', 'code_comment'),                          # Comentários linha
            (r'/\*[\s\S]*?\*/', 'code_comment'),                 # Comentários bloco
            (r'(["\'])(?:(?!\1|\\).|\\.)*\1', 'code_string'),   # Strings
            (r'`[^`]*`', 'code_string'),                         # Template literals
            (r'\b(\d+\.?\d*)\b', 'code_number'),                 # Números
            (r'\bfunction\s+(\w+)', 'code_function'),            # Funções
            (r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', 'code_function'),  # Arrow functions
        ]
        
        lines = code.split('\n')
        for line in lines:
            self._highlight_line(line, patterns, self.JS_KEYWORDS)
            self.insert(tk.END, '\n', 'code_block')
    
    def _highlight_line(self, line: str, patterns: list, keywords: set):
        """Aplica highlighting a uma linha"""
        if not line:
            return
        
        # Encontrar todas as correspondências
        highlights = []  # (start, end, tag)
        
        for pattern, tag in patterns:
            for match in re.finditer(pattern, line, re.MULTILINE):
                highlights.append((match.start(), match.end(), tag))
        
        # Adicionar palavras-chave
        for keyword in keywords:
            pattern = rf'\b{re.escape(keyword)}\b'
            for match in re.finditer(pattern, line):
                highlights.append((match.start(), match.end(), 'code_keyword'))
        
        # Ordenar e remover sobreposições
        highlights.sort(key=lambda x: (x[0], -x[1]))
        filtered = []
        last_end = 0
        for start, end, tag in highlights:
            if start >= last_end:
                filtered.append((start, end, tag))
                last_end = end
        
        # Inserir texto com highlighting
        last_pos = 0
        for start, end, tag in filtered:
            if start > last_pos:
                self.insert(tk.END, line[last_pos:start], 'code_block')
            self.insert(tk.END, line[start:end], ('code_block', tag))
            last_pos = end
        
        if last_pos < len(line):
            self.insert(tk.END, line[last_pos:], 'code_block')
    
    def _insert_table(self, table_lines: list):
        """Insere uma tabela usando um widget real (Frame + Grid) para alinhamento perfeito"""
        if len(table_lines) < 2:
            return
        
        # Parse headers
        header_line = table_lines[0].strip()
        if header_line.startswith('|'): header_line = header_line[1:]
        if header_line.endswith('|'): header_line = header_line[:-1]
        headers = [cell.strip() for cell in header_line.split('|')]
        
        # Parse rows
        rows = []
        for line in table_lines[2:]:
            line = line.strip()
            if line.startswith('|'): line = line[1:]
            if line.endswith('|'): line = line[:-1]
            cells = [cell.strip() for cell in line.split('|')]
            if cells and any(c for c in cells):
                rows.append(cells)

        # Criar um container para a tabela
        # O bg aqui define a cor da "borda" entre as células
        table_frame = tk.Frame(self, bg='#bdc3c7', padx=0, pady=0)
        
        # Adicionar cabeçalhos
        for col, header in enumerate(headers):
            lbl = tk.Label(table_frame, text=header, font=('Segoe UI', 10, 'bold'),
                          bg='#e9ecef', fg='#212529', padx=10, pady=5, 
                          relief='flat', anchor='w')
            lbl.grid(row=0, column=col, sticky='nsew', padx=1, pady=1)
            
        # Adicionar linhas de dados
        for row_idx, row in enumerate(rows):
            for col_idx in range(len(headers)):
                cell_text = row[col_idx] if col_idx < len(row) else ""
                bg_color = '#f8f9fa' if row_idx % 2 == 1 else '#ffffff'
                lbl = tk.Label(table_frame, text=cell_text, font=('Segoe UI', 10),
                              bg=bg_color, fg='#333333', padx=10, pady=5,
                              relief='flat', anchor='w')
                lbl.grid(row=row_idx + 1, column=col_idx, sticky='nsew', padx=1, pady=1)

        # Forçar colunas a terem peso para distribuir espaço se necessário
        for col in range(len(headers)):
            table_frame.columnconfigure(col, weight=1)

        # Inserir o widget da tabela dentro do Text
        self.insert(tk.END, '\n')
        self._textbox.window_create(tk.END, window=table_frame)
        self.insert(tk.END, '\n')
    
    def _insert_sample(self):
        """Insere texto de exemplo"""
        sample = '''# 🎉 Renderizador Markdown para Tkinter

Este é um **componente nativo** para visualizar *Markdown* em tempo real!

## ✨ Formatação de Texto

- **Texto em negrito** usando `**texto**`
- *Texto em itálico* usando `*texto*`
- ***Negrito e itálico*** usando `***texto***`
- ~~Texto riscado~~ usando `~~texto~~`
- `Código inline` usando crases

## 📝 Listas

### Lista não ordenada:
- Item principal
  - Sub-item
  - Outro sub-item
      - Sub-sub-item
- Segundo item
- Terceiro item

### Lista ordenada:
1. Primeiro passo
2. Segundo passo
3. Terceiro passo

### Checkboxes:
- [x] Tarefa concluída
- [ ] Tarefa pendente
- [x] Outra tarefa feita

## 💬 Citações

> "A simplicidade é a sofisticação máxima."
> — Leonardo da Vinci

## 💻 Blocos de Código

### Python:
```python
def fibonacci(n):
    """Calcula o n-ésimo número de Fibonacci"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Exemplo de uso
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

### JavaScript:
```javascript
// Função assíncrona moderna
const fetchData = async (url) => {
    const response = await fetch(url);
    const data = await response.json();
    console.log("Dados recebidos:", data);
    return data;
};

fetchData("https://api.exemplo.com/dados");
```

## 📊 Tabelas

| Linguagem | Tipo | Popularidade |
|-----------|------|--------------|
| Python | Dinâmica | ⭐⭐⭐⭐⭐ |
| JavaScript | Dinâmica | ⭐⭐⭐⭐⭐ |
| Rust | Estática | ⭐⭐⭐⭐ |
| Go | Estática | ⭐⭐⭐⭐ |

---

## 🔗 Links

Visite o [Python.org](https://python.org) para mais informações!

---

**Divirta-se escrevendo em Markdown!** 🚀
'''
        self._render_markdown(sample)