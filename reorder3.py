import re

with open('d:/Website/pear/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the members section bounds
sec_start = content.find('<h2 class="section-title">Anggota Laboratorium</h2>')
start_idx = content.find('<!--', sec_start)
end_idx = content.find('    </div>\n</section>', start_idx)

if start_idx == -1 or end_idx == -1:
    print('Markers not found')
    exit(1)

blocks_text = content[start_idx:end_idx]

# Split by block markers (any HTML comment that indicates a new block)
parts = re.split(r'\s*(?=<!--(?: Kolaborator| Kepala Lab| Kepala KBK))', blocks_text)
# Filter empty parts
parts = [p.strip() for p in parts if p.strip()]

# Find which part belongs to which person by checking the name in the text
blocks = {}
for p in parts:
    if 'Fahmizal' in p:
        blocks['Fahmizal'] = p
    elif 'Adhiim' in p:
        blocks['Adhiim'] = p
    elif 'Jimmy' in p:
        blocks['Jimmy'] = p
    elif 'Maun' in p or "Ma'un" in p:
        blocks['Maun'] = p
    elif 'Adlan' in p:
        blocks['Adlan'] = p
    elif 'Candra' in p or 'Chandra' in p:
        blocks['Candra'] = p
    elif 'Alvin' in p:
        blocks['Alvin'] = p

# Check if we have all 7
print('Found blocks:', list(blocks.keys()))

jimmy_block = blocks['Jimmy']
jimmy_block = re.sub(r'(Kolaborator|Ketua Lab)</div>', 'Kepala KBK</div>', jimmy_block)
jimmy_block = re.sub(r'<!--.*?-->', '<!-- Kepala KBK: Dr. Ir. Jimmy Trio Putra -->', jimmy_block, count=1)

adhiim_block = blocks['Adhiim']
adhiim_block = re.sub(r'(Kolaborator|Kepala KBK)</div>', 'Ketua Lab</div>', adhiim_block)
adhiim_block = re.sub(r'<!--.*?-->', '<!-- Ketua Lab: Ahmad Adhiim Muthahhari -->', adhiim_block, count=1)

def set_style(block, is_first):
    # Remove existing classes
    block = block.replace('reveal-delay-2', 'reveal-delay-1') if is_first else block.replace('reveal-delay-1', 'reveal-delay-2')
    
    # Margin
    block = block.replace('margin: 32px auto 0', 'margin: 40px auto 0') if is_first else block.replace('margin: 40px auto 0', 'margin: 32px auto 0')
    
    # Colors
    if is_first:
        if 'var(--gray-light)' in block: block = block.replace('var(--gray-light)', 'var(--sky)')
        if 'var(--gray-dark)' in block: block = block.replace('var(--gray-dark)', 'var(--blue)')
        if 'rgba(0,0,0,0.08)' in block: block = block.replace('rgba(0,0,0,0.08)', 'rgba(7,60,100,0.12)')
    else:
        if 'var(--sky)' in block: block = block.replace('var(--sky)', 'var(--gray-light)')
        if 'var(--blue)' in block: block = block.replace('var(--blue)', 'var(--gray-dark)')
        if 'rgba(7,60,100,0.12)' in block: block = block.replace('rgba(7,60,100,0.12)', 'rgba(0,0,0,0.08)')
    return block

ordered_blocks = [
    set_style(jimmy_block, True),
    set_style(adhiim_block, False),
    set_style(blocks['Maun'], False),
    set_style(blocks['Fahmizal'], False),
    set_style(blocks['Adlan'], False),
    set_style(blocks['Candra'], False),
    set_style(blocks['Alvin'], False)
]

new_blocks_text = '\n\n        '.join(ordered_blocks) + '\n'
new_content = content[:start_idx] + new_blocks_text + content[end_idx:]

with open('d:/Website/pear/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Success')
