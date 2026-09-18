# 🛡️ TokenShield-UI: Smart UI Proxy & Grounding Middleware
### *By Aethelion (Korhan)*

> **Otonom yapay zeka ajanlarının (AI Agents) işletim sistemini ve uygulamaları yönetirken ekran görüntüsüyle token'ları tüketmesini engelleyen, yerel GPU destekli akıllı filtre, D-Pad navigasyon motoru ve devre kesici (Circuit Breaker) katmanı.**

[![GitHub Repo](https://img.shields.io/badge/GitHub-TokenShield--UI-181717?logo=github)](https://github.com/KorhanWithSunglasses/TokenShield-UI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-CUDA%20Ready-red.svg)](https://pytorch.org/)
[![Model](https://img.shields.io/badge/Model-Microsoft%20Florence--2-green.svg)](https://huggingface.co/microsoft/Florence-2-base)
[![MCP](https://img.shields.io/badge/Protocol-FastMCP%20Standard-purple.svg)]()
[![Token Savings](https://img.shields.io/badge/Token%20Savings-%20~97.5%25-brightgreen.svg)]()

---

> ⚠️ **Bu Dökümantasyon Çift Modludur (Dual-Audience Documentation):**
> * 👤 **Bölüm 1: Eğer bir İnsan Geliştirici okuyorsa** (Sistemin mantığı, token krizi çözümü, kurulum ve kullanım rehberi).
> * 🤖 **Bölüm 2: Eğer bir Yapay Zeka / AI Ajanı okuyorsa** (Doğrudan ajan sistem promptu, MCP araç entegrasyonu, hata kurtarma ve karar protokolleri).

---

## 👤 BÖLÜM 1: EĞER BU BELGEYİ BİR İNSAN OKUYORSA

### 📌 Problem Nedir? Neden Bu Projeyi Yazdım?
Son dönemde popülerleşen otonom yapay zeka ajanları (**OpenClaw, Anthropic Computer Use, Vision Ajanları vb.**), bilgisayarınızı veya emülatörünüzü yönetirken her tıklamada ekran görüntüsü alır.

Bu yaklaşım pratikte **iki büyük felakete** yol açar:
1. **Aşırı Token Tüketimi (Token Bleeding):**  
   1080p veya 4K tek bir ekran görüntüsü, LLM'e (GPT-4o, Claude vb.) gönderildiğinde **1.500 ile 2.500 token** harcar. Basit bir 40 adımlık form doldurma veya menü testi, dakikalar içinde **100.000+ token** yakarak cüzdanınızı boşaltır.
2. **Kilitlenme ve Sonsuz Döngü Tuzağı (Loop Trap):**  
   Uygulama çöktüğünde veya buton tepki vermediğinde ajan bunu görsel olarak fark edemez; inatla aynı butona tekrar tekrar tıklar ve siz farkına varana kadar arkada yüzlerce dolar harcar.

### 💡 TokenShield-UI Nasıl Çözüyor?
* **Gözler Bilgisayarınızda (Yerel GPU):** Ekran resimleri bulut LLM'e **ASLA** gitmez. Bilgisayarınızdaki yerel model (**Microsoft Florence-2-base**, sadece ~680 MB VRAM) ekranı saniyenin onda birinde tarar.
* **Ajana Sadece Metin Gider:** LLM'in önüne devasa bir resim yerine, sadece tıklanabilir öğeleri ve odak bilgisini içeren küçücük bir JSON haritası sunulur (**~45 token**).
* **pHash Devre Kesici (Circuit Breaker):** Sistem ekranın dijital parmak izini (*Perceptual Hash*) takip eder. Üst üste 3 işlem boyunca ekranda değişiklik olmazsa sistemi kilitler ve ajanın token yakmasını durdurur.
* **Android TV / TvBox & BlueStacks Desteği:** Mavi/Cyan kumanda odak çerçevelerini tespit eder ve otomatik kumanda tuşları (`DPAD_UP`, `DPAD_RIGHT`, `DPAD_CENTER`) üretir.
* **Arka Planda Sessiz Çalışma:** BlueStacks arkadayken veya simge durumundayken farenizi oynatmadan, pencerelerinizi kapatmadan çalışır.

### 📊 Token & Maliyet Karşılaştırması

| Kriter | Klasik Vision Ajanları (OpenClaw vb.) | TokenShield-UI (Aethelion) |
| :--- | :--- | :--- |
| **Görsel İşleme Yeri** | Bulut LLM (Ücretli API) | **Yerel Ekran Kartı (RTX / CUDA / CPU - Ücretsiz)** |
| **Tıklama Başına Token** | ~1.800 - 2.500 Token | **~40 - 60 Token (JSON)** |
| **50 Adımlık Test Maliyeti** | ~100.000 Token (~1.20$) | **~2.500 Token (~0.02$)** |
| **Tasarruf Oranı** | - | **%97.5 AZALMA 🎯** |
| **Donma / Loop Koruması** | Yok (Sonsuz döngüye girer) | **Var (pHash Circuit Breaker 3. adımda durdurur)** |

---

### 🚀 İnsan Geliştirici İçin Kurulum & Kullanım

#### 1. Depoyu Klonlayın ve Bağımlılıkları Yükleyin
```bash
git clone https://github.com/KorhanWithSunglasses/TokenShield-UI.git
cd TokenShield-UI

# Bağımlılıkları yükleyin (CUDA destekli PyTorch önerilir)
pip install -r requirements.txt
```

#### 2. Tek Tıkla Aç/Kapat (Toggle Switch)
Sistemi dilediğiniz an tek tıkla devre dışı bırakmak veya tekrar açmak için:
* Depo içindeki **`toggle_shield.bat`** dosyasına çift tıklayın. Anında açılır/kapanır.

#### 3. MCP Olarak Ekleyin (Cursor, Antigravity, Claude Desktop, Windsurf)
Kullandığınız aracın MCP konfigürasyon dosyasına (`mcp_config.json` veya `claude_desktop_config.json`) şu bloğu ekleyin:

```json
{
  "mcpServers": {
    "smart-ui-proxy": {
      "command": "python",
      "args": [
        "C:\\TAM_YOL\\TokenShield-UI\\server.py"
      ],
      "env": {}
    }
  }
}
```

---

## 🤖 BÖLÜM 2: EĞER BU BELGEYİ BİR YAPAY ZEKA / AI AJANI OKUYORSA
*(FOR AUTONOMOUS AI AGENTS, CURSOR AGENT, ANTIGRAVITY, CLAUDE DESKTOP)*

```yaml
agent_instruction_type: system_guidelines
target_agent: LLM / Autonomous Agent / Coding Assistant
middleware_name: TokenShield-UI
protocol: Model Context Protocol (MCP)
primary_objective: Zero-token-waste GUI perception, background execution, loop prevention
```

### 🎯 Ajan Karar Protokolü (Operational Directives)

Eğer kullanıcı senden işletim sisteminde (Windows Masaüstü) veya bir Android emülatöründe (BlueStacks / TvBox) bir işlem yapmanı istediyse, **AŞAĞIDAKİ PROTOKOLÜ HARFİYEN UYGULA:**

#### 1. ASLA Ham Ekran Görüntüsü ÇAĞIRMA:
* `screenshot` veya `take_screenshot` araçlarını çağırma. 
* Bu araçlar bağlamını 2.000+ tokenlik görsellerle doldurur ve kullanıcının API kredisini tüketir.
* Bunun yerine her zaman **`smart_ui_scan`** aracını çağır.

#### 2. Ekran Taramasını Yorumlama (`smart_ui_scan`):
* `smart_ui_scan(source="bluestacks"|"desktop")` çağırdığında sana şu formatta temiz bir JSON dönecektir:
  ```json
  {
    "screen_dimensions": [1920, 1080],
    "active_focus": {
      "box": [47, 540, 285, 883],
      "center": [166, 711],
      "status": "Cyan Highlight Verified"
    },
    "cards": [
      {"box": [624, 98, 753, 310], "center": [688, 204]},
      {"box": [790, 98, 1013, 368], "center": [901, 233]}
    ]
  }
  ```
* Bu JSON üzerindeki koordinatları doğrudan aksiyonlarında kullan.

#### 3. Aksiyon Alma Protokolü (`smart_ui_click`):
* **TvBox / Android TV Odaklı Gezinme:** Eğer `active_focus` alanı doluysa, hedef karta gitmek için `method="dpad"` ve hesaplanan `dpad_steps` (örn: `["DPAD_UP", "DPAD_RIGHT", "DPAD_CENTER"]`) parametrelerini gönder.
* **Doğrudan Tıklama:** Masaüstü veya dokunmatik arayüzlerde `method="tap"` ve `coords=[x, y]` gönder.

#### 4. Kilitlenme ve Hata Yönetimi (`CIRCUIT_BREAKER`):
* Eğer araç sana şu yanıtı dönerse:
  ```json
  {"status": "CIRCUIT_BREAKER_TRIGGERED", "error": "Ekran son 3 aksiyondur degismedi..."}
  ```
  * **ASLA aynı butona tekrar tıklamayı deneme!**
  * Döngüyü derhal durdur.
  * Kullanıcıya ekranın donduğunu veya uygulamanın yanıt vermediğini raporla.
  * Kullanıcı onay verdikten sonra `smart_ui_reset()` aracını çağırarak kilidi kaldır.

#### 5. Masaüstü Kısayollarına Doğrudan Erişim (`smart_ui_desktop_items`):
* Kullanıcı masaüstündeki bir programı açmanı istediğinde ekrandaki pencereleri küçültme.
* Doğrudan `smart_ui_desktop_items(launch="Uygulama Adi")` aracını çağır. Bu, farenin kontrolünü çalmadan uygulamayı arka planda ayağa kaldırır.

---

## 📁 Proje Dizin Yapısı

```
TokenShield-UI/
├── engine.py              # Çekirdek görsel motor (Florence-2, OpenCV, Cyan Odak)
├── fallback_handler.py    # Donma koruması, pHash parmak izi ve Circuit Breaker
├── agent_ui_tool.py       # Terminalden çalıştırma ve benchmark CLI aracı
├── server.py              # FastMCP JSON-RPC sunucusu
├── toggle_shield.py       # Tek tıkla aç/kapat motoru
├── toggle_shield.bat      # Windows çift tıkla aç/kapat başlatıcısı
├── requirements.txt       # Python paket bağımlılıkları
├── .gitignore             # Git yoksayma kuralları
├── LICENSE                # MIT Lisansı
└── README.md              # Çift modlu detaylı dökümantasyon
```

---

## 📄 Lisans & Yazar

* **Yazar:** Aethelion (Korhan)
* **Lisans:** Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır. Dilediğiniz gibi ticari veya kişisel projelerinizde kullanabilir, geliştirebilir ve paylaşabilirsiniz.
