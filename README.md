# 🛡️ Audit Static pentru Proiecte Python

Acest script efectuează un **audit static de bază** asupra unui proiect Python, folosind unelte populare pentru analiza codului, verificări de securitate și evaluarea mentenabilității.

## 🔍 Ce face scriptul?

Rulează automat următoarele unelte:

- `flake8` – verifică stilul PEP8 și erorile de sintaxă.
- `bandit` – analizează codul pentru vulnerabilități de securitate.
- `pip-audit` – verifică dependențele pentru CVE-uri cunoscute.
- `radon` – măsoară complexitatea ciclomatică și mentenabilitatea.
- `black` – verifică dacă formatarea codului respectă standardele.
- `isort` – verifică dacă importurile sunt sortate corect.

Output-ul este afișat în consolă și salvat într-un fișier text, de forma:
```
raport_audit_YYYYMMDD_HHMMSS.txt
```

## ⚙️ Instalare

Asigură-te că ai Python 3 instalat, apoi instalează uneltele necesare:

```bash
pip install flake8 bandit pip-audit radon black isort
```

## ▶️ Utilizare

```bash
python audit.py /calea/catre/proiect
```

- Dacă nu specifici calea, se va analiza directorul curent.
- Se va genera automat un fișier `.txt` cu raportul complet.

### Exemplu:

```bash
python audit.py ~/proiecte/aplicatie/
```

## 🧾 Exemplu de output

```
===== FLAKE8 (LINTER PEP8 & ERORI) =====
Output:
main.py:10:1: F401 'os' imported but unused

[FAILED/WARNING] Flake8 a terminat cu codul 1. Verifică output-ul.

===== RADON - COMPLEXITATE CICLOMATICĂ =====
Output:
main.py - A (1.00)
utils.py - B (4.00)

[PASSED] Radon a rulat cu succes.
```

## ⚠️ Limitări

- Nu înlocuiește un audit complet de securitate.
- Nu verifică configurații CI/CD, permisiuni la fișiere sau testare runtime.
- Poate genera false negative / false positive.
- Necesită unelte externe instalate în PATH.

## 📄 Licență

Distribuit sub licența MIT – vezi [LICENSE](LICENSE) pentru detalii.
