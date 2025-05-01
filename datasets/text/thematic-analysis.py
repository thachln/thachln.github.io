# Cài các phần mềm
# pip install requests beautifulsoup4 nltk matplotlib seaborn networkx
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
import string

# Cài đặt 1 lần
# nltk.download('punkt')
# nltk.download('stopwords')

# BƯỚC 1: Tải và tiền xử lý văn bản
url = "https://thachln.github.io/datasets/text/Toàn văn phát biểu của TBT ngày 30-4-2025.txt"
response = requests.get(url)
text = BeautifulSoup(response.text, 'html.parser').get_text()

# BƯỚC 2: Mã hóa sơ bộ (tokenize & lọc stopwords)
# Để sử dụng stopwords tiếng Việt thì hãy tải file tại
# “raw.githubusercontent.com/stopwords/vietnamese-stopwords/refs/heads/master/vietnamese-stopwords.txt”
# và lưu vào %USERPROFILE%\AppData\Roaming\nltk_data\corpora\stopwords.
# Chú ý lưu thành file “vietnamese” không có phần đuôi .txt.

stop_words = set(stopwords.words('vietnamese') + list(string.punctuation))
sentences = sent_tokenize(text)
codes = defaultdict(list)

for i, sent in enumerate(sentences):
    words = word_tokenize(sent.lower())
    keywords = [w for w in words if w not in stop_words and w.isalpha()]
    for kw in keywords:
        codes[kw].append((i, sent))

# BƯỚC 3: Gán mã vào chủ đề (dựa theo từ khóa)
# theme_keywords = {
#     "Tiến bộ và phát triển": ["phát triển", "tiến bộ", "hiện đại", "công nghệ", "đổi mới"],
#     "Hòa hợp dân tộc": ["hòa hợp", "đoàn kết", "dân tộc", "thống nhất", "đồng lòng"],
#     "Định hướng tương lai": ["tương lai", "mục tiêu", "chiến lược", "định hướng", "nhiệm vụ"],
#     "Chủ nghĩa anh hùng": ["anh hùng", "chiến đấu", "hy sinh", "dũng cảm", "kiên cường"]
# }
# Từ khóa gợi ý cho chủ đề mới
theme_keywords = {
    "Đoàn kết dân tộc": ["đoàn kết", "gắn bó", "đồng lòng", "thống nhất", "liên kết", "tập thể", "hợp tác"],
    "Hòa hợp dân tộc": ["hòa hợp", "hòa giải", "giao lưu", "giao thoa", "đa dạng", "khác biệt", "chung sống"],
    "Tiến bộ và phát triển": ["phát triển", "tiến bộ", "cải tiến", "hiện đại hóa", "đổi mới", "tăng trưởng"],
    "Định hướng tương lai": ["tương lai", "chiến lược", "kế hoạch", "tầm nhìn", "phát triển bền vững", "dài hạn", "hướng tới"],
    "Chủ nghĩa anh hùng": ["anh hùng", "hy sinh", "quyết tử", "dũng cảm", "kiên cường", "chiến đấu", "tự hào"]
}


themes = defaultdict(list)

for theme, keywords in theme_keywords.items():
    for kw in keywords:
        if kw in codes:
            themes[theme].extend(codes[kw])

# BƯỚC 4: Rà soát chủ đề (loại trùng lặp câu)
for theme in themes:
    themes[theme] = list(set([s for _, s in themes[theme]]))

# BƯỚC 5: Mô tả chủ đề (tùy chỉnh theo ngữ cảnh)
# theme_descriptions = {
#     "Tiến bộ và phát triển": "Các nội dung liên quan đến đổi mới, phát triển đất nước, hiện đại hóa.",
#     "Hòa hợp dân tộc": "Nội dung về sự đoàn kết, thống nhất, hòa bình giữa các thành phần trong xã hội.",
#     "Định hướng tương lai": "Tầm nhìn, chiến lược cho tương lai, kế hoạch và mục tiêu quốc gia.",
#     "Chủ nghĩa anh hùng": "Tinh thần chiến đấu, hy sinh, lòng quả cảm trong lịch sử và hiện tại."
# }
theme_descriptions = {
    "Đoàn kết dân tộc": "Tập trung vào các thông điệp về sự đồng lòng, thống nhất và liên kết giữa các tầng lớp, vùng miền và dân tộc trong toàn quốc.",

    "Hòa hợp dân tộc": "Đề cập đến sự chung sống hòa bình, chấp nhận sự đa dạng và kêu gọi hòa giải, hoà hợp giữa các khác biệt trong cộng đồng dân tộc Việt Nam.",

    "Tiến bộ và phát triển": "Nội dung thể hiện sự cải tiến, đổi mới, hiện đại hóa đất nước và nỗ lực không ngừng để đạt được các thành tựu kinh tế, xã hội, khoa học, công nghệ.",

    "Định hướng tương lai": "Những tầm nhìn chiến lược, mục tiêu dài hạn và các kế hoạch phát triển bền vững hướng tới xây dựng tương lai cho đất nước.",

    "Chủ nghĩa anh hùng": "Tôn vinh tinh thần quả cảm, sự hy sinh, kiên cường và lòng yêu nước của nhân dân trong các cuộc đấu tranh bảo vệ tổ quốc."
}

# BƯỚC 6: Xuất kết quả ra màn hình
print("\n==================== PHÂN TÍCH CHỦ ĐỀ ====================")
for theme, sentences in themes.items():
    print(f"\n🔸 Chủ đề: {theme}")
    print(f"  👉 Mô tả: {theme_descriptions[theme]}")
    print(f"  🔍 Số câu liên quan: {len(sentences)}")
    print("  📝 Một vài ví dụ:")
    for s in sentences[:3]:
        print("     ➤", s.strip())


#####
import matplotlib.pyplot as plt
import seaborn as sns

# Đếm tần suất từ khóa trong văn bản theo từng chủ đề
keyword_frequencies = {}

for theme, keywords in theme_keywords.items():
    keyword_frequencies[theme] = {}
    for kw in keywords:
        keyword_frequencies[theme][kw] = sum(1 for s in sentences if kw in s.lower())

# Thiết lập style cho biểu đồ
sns.set(style="whitegrid")
num_themes = len(theme_keywords)
fig, axes = plt.subplots(num_themes, 1, figsize=(10, 5 * num_themes), constrained_layout=True)

if num_themes == 1:
    axes = [axes]  # nếu chỉ có 1 biểu đồ

for i, (theme, freq_dict) in enumerate(keyword_frequencies.items()):
    ax = axes[i]
    kws = list(freq_dict.keys())
    freqs = list(freq_dict.values())

    sns.barplot(x=freqs, y=kws, ax=ax, palette="viridis")
    ax.set_title(f"Tần suất từ khóa - Chủ đề: {theme}", fontsize=14, pad=10)
    ax.set_xlabel("Số lần xuất hiện", fontsize=12, labelpad=10)
    ax.set_ylabel("Từ khóa", fontsize=12)

    # Hiển thị giá trị trên từng cột
    for j, val in enumerate(freqs):
        ax.text(val + 0.5, j, str(val), va='center', fontsize=10)

# Không cần tight_layout nếu dùng constrained_layout
# plt.show()

##########
import networkx as nx
import matplotlib.pyplot as plt

# Khởi tạo đồ thị
G = nx.Graph()

# Node trung tâm
central_node = "Thông điệp bài viết TBT Tô Lâm"
G.add_node(central_node, type='central')

# Thêm chủ đề và liên kết với node trung tâm
for theme in theme_keywords:
    G.add_node(theme, type='theme')
    G.add_edge(central_node, theme)

# Thêm từ khóa cho mỗi chủ đề
for theme, keywords in theme_keywords.items():
    for kw in keywords:
        G.add_node(kw, type='keyword')
        G.add_edge(theme, kw)

# Layout: tăng khoảng cách giữa các node
pos = nx.spring_layout(G, k=1.2, iterations=100, seed=42)

# Màu và kích thước node theo loại
node_colors = []
node_sizes = []

for n in G.nodes:
    ntype = G.nodes[n]['type']
    if ntype == 'central':
        node_colors.append('orange')
        node_sizes.append(3000)
    elif ntype == 'theme':
        node_colors.append('skyblue')
        node_sizes.append(2000)
    else:
        node_colors.append('lightgreen')
        node_sizes.append(1200)

# Vẽ đồ thị
plt.figure(figsize=(16, 12))
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes,
        font_size=10, font_family="Arial", edge_color='gray', font_weight='bold')

plt.title("Sơ đồ mạng chủ đề và từ khóa – Phát biểu của TBT Tô Lâm", fontsize=16)
plt.axis("off")
plt.tight_layout()
plt.show()
