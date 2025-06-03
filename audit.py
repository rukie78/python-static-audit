#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pentru Audit Static de Bază al unei Aplicații Python.

Acest script rulează o serie de unelte de analiză statică pentru a verifica
calitatea codului, potențiale probleme de securitate și complexitatea.
Output-ul este afișat în consolă și salvat într-un fișier raport_audit_YYYYMMDD_HHMMSS.txt.

PRECONDIȚII:
Asigură-te că ai instalat următoarele unelte Python în mediul tău:
  pip install flake8 bandit pip-audit radon black isort

UTILIZARE:
  python audit_script_v2.py /calea/catre/proiectul/tau
  Dacă nu specifici calea, va încerca să ruleze în directorul curent.

LIMITĂRI:
- Acest script NU este un audit complet de securitate sau de conformitate.
- Este un punct de pornire și automatizează doar anumite verificări statice.
- Revizuirea manuală și testarea dinamică sunt în continuare esențiale.
"""

import subprocess
import argparse
import os
import sys
import datetime

# Definește comenzile de rulat
COMMANDS_TO_RUN = [
    ("Flake8 (Linter PEP8 & Erori)", ["flake8", "{project_path}"]),
    ("Bandit (SAST Securitate Python)", ["bandit", "-r", "{project_path}", "-f", "txt"]),
    ("pip-audit (Vulnerabilități Dependințe)", ["pip-audit"]),
    ("Radon - Complexitate Ciclomatică", ["radon", "cc", "{project_path}", "-a", "-s"]),
    ("Radon - Indice Mentenabilitate", ["radon", "mi", "{project_path}", "-s"]),
    ("Black (Verificare Formatare Cod)", ["black", "--check", "--diff", "{project_path}"]),
    ("isort (Verificare Sortare Importuri)", ["isort", "--check-only", "--diff", "{project_path}"]),
]

def log_message(message, report_file_handle):
    """Scrie mesajul în consolă și în fișierul de raport."""
    print(message)
    if report_file_handle:
        report_file_handle.write(message + "\n")

def log_header(title, report_file_handle):
    """Afișează un antet formatat în consolă și fișier."""
    header_line = "\n" + "=" * 70
    title_line = f"===== {title.upper()} ====="
    log_message(header_line, report_file_handle)
    log_message(title_line, report_file_handle)
    log_message(header_line, report_file_handle)

def log_tool_output(tool_name, output, error, return_code, report_file_handle):
    """Afișează output-ul unei unelte în consolă și fișier."""
    separator = "-" * 50
    log_message(f"\n--- Rezultate pentru: {tool_name} ---", report_file_handle)
    if output:
        log_message("Output:\n" + output, report_file_handle)
    if error:
        log_message("Erori (dacă există):\n" + error, report_file_handle)
    
    status_message = ""
    if return_code == 0:
        status_message = f"[PASSED] {tool_name} a rulat cu succes (cod ieșire 0)."
    else:
        status_message = f"[FAILED/WARNING] {tool_name} a terminat cu codul {return_code}. Verifică output-ul."
    log_message(status_message, report_file_handle)
    log_message(separator, report_file_handle)

def run_command(tool_name, command_template, project_path, report_file_handle):
    """Rulează o comandă specifică și înregistrează output-ul."""
    command = [arg.replace("{project_path}", project_path) if isinstance(arg, str) else arg for arg in command_template]

    if tool_name == "pip-audit (Vulnerabilități Dependințe)":
        log_header(f"Rulare {tool_name} (asigură-te că mediul virtual al proiectului este activat)", report_file_handle)
    else:
        log_header(f"Rulare {tool_name} pentru calea: {project_path}", report_file_handle)

    try:
        # Folosim encoding='utf-8', errors='replace' pentru a gestiona caracterele neașteptate
        process = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8', errors='replace')
        log_tool_output(tool_name, process.stdout, process.stderr, process.returncode, report_file_handle)
        return process.returncode
    except FileNotFoundError:
        error_msg_fnf = f"[ERROR] Comanda pentru '{tool_name}' nu a fost găsită. Asigură-te că unealta este instalată și în PATH.\nComanda încercată: {' '.join(command)}"
        log_message(error_msg_fnf, report_file_handle)
        return -1 
    except Exception as e:
        error_msg_exc = f"[ERROR] A apărut o eroare la rularea '{tool_name}': {e}\nComanda încercată: {' '.join(command)}"
        log_message(error_msg_exc, report_file_handle)
        return -2

def main():
    parser = argparse.ArgumentParser(description="Script de audit static de bază pentru aplicații Python.")
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Calea către directorul rădăcină al proiectului Python de auditat. Default: directorul curent."
    )
    args = parser.parse_args()

    project_path = os.path.abspath(args.project_path)

    if not os.path.isdir(project_path):
        print(f"[ERROR] Calea specificată '{project_path}' nu este un director valid.")
        sys.exit(1)
        
    # Generare nume fișier raport cu timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"raport_audit_{timestamp}.txt"
    report_filepath = os.path.join(os.getcwd(), report_filename) # Salvează în directorul curent unde rulează scriptul

    try:
        with open(report_filepath, 'w', encoding='utf-8') as report_file:
            initial_info = f"Inițiere audit static pentru proiectul din: {project_path}\n" \
                           f"Raport generat la: {timestamp}\n" \
                           "Asigură-te că toate uneltele necesare (Flake8, Bandit, etc.) sunt instalate."
            log_message(initial_info, report_file)

            results_summary = {}

            for tool_name, command_template in COMMANDS_TO_RUN:
                return_code = run_command(tool_name, command_template, project_path, report_file)
                results_summary[tool_name] = return_code
            
            log_header("Sumar Audit (Coduri de Ieșire)", report_file)
            all_passed_strict = True # Devine False dacă orice cod nu e 0
            any_tool_missing_or_script_error = False # Devine True dacă vreo unealtă lipsește sau apare eroare de script

            for tool, code in results_summary.items():
                status_text = ""
                if code == 0:
                    status_text = "OK/Verifică Output"
                elif code == -1: # Unealtă lipsă
                    status_text = "EROARE SCRIPT (Unealtă lipsă)"
                    all_passed_strict = False
                    any_tool_missing_or_script_error = True
                elif code == -2: # Altă eroare de script la rularea uneltei
                    status_text = "EROARE SCRIPT (Problemă la rulare)"
                    all_passed_strict = False
                    any_tool_missing_or_script_error = True
                else: # Unealta a rulat dar a returnat eroare/avertisment
                    status_text = f"EROARE/AVERTISMENT (cod {code})"
                    all_passed_strict = False
                log_message(f"- {tool}: {status_text}", report_file)
            
            summary_footer_message = ""
            if all_passed_strict:
                summary_footer_message = "\nToate uneltele de audit automat au rulat și au returnat codul 0 (ceea ce indică de obicei absența problemelor detectabile automat sau formatare corectă)."
            elif not any_tool_missing_or_script_error and not all_passed_strict:
                 summary_footer_message = "\nUnele unelte au raportat probleme (cod de ieșire non-zero). Verifică output-ul de mai sus și din fișier pentru detalii."
            else: # Daca au fost erori de script
                summary_footer_message = "\nAu apărut erori la rularea scriptului sau unele unelte lipsesc. Verifică output-ul de mai sus și din fișier pentru detalii."

            log_message(summary_footer_message, report_file)
            log_message("IMPORTANT: Verifică manual output-ul fiecărei unelte pentru detalii și posibile false pozitive/negative.", report_file)
            
            final_audit_message = f"\nAudit static de bază finalizat.\n" \
                                  f"Raportul a fost salvat în: {report_filepath}\n" \
                                  "Nu uita că acesta este doar un punct de pornire. Auditul manual și testarea dinamică sunt esențiale."
            log_message(final_audit_message, report_file)
            # Afișează și în consolă calea către raport, la final
            print(f"\nRaportul a fost salvat în: {report_filepath}")

    except IOError as e:
        print(f"[EROARE FATALĂ] Nu s-a putut scrie în fișierul de raport '{report_filepath}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[EROARE FATALĂ] O eroare neașteptată a apărut: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
