# 4. Master-Liste (All-in-One) finalisieren und splitten
    if master_domains:
        final_master = sorted(list(master_domains))
        limit = 1200000
        
        # --- PART 1 erstellen ---
        part1 = final_master[:limit]
        with open("combined_part1.txt", 'w', encoding='utf-8') as f:
            f.write("### TechRZN - MASTER BLOCKLIST PART 1 ###\n")
            f.write(f"### Rules in this part: {len(part1)} ###\n\n")
            for d in part1:
                f.write(f"||{d}^\n")
        print(f"✅ combined_part1.txt erstellt ({len(part1)} Domains).")

        # --- PART 2 erstellen (der Rest) ---
        part2 = final_master[limit:]
        if part2:
            with open("combined_part2.txt", 'w', encoding='utf-8') as f:
                f.write("### TechRZN - MASTER BLOCKLIST PART 2 ###\n")
                f.write(f"### Rules in this part: {len(part2)} ###\n\n")
                for d in part2:
                    f.write(f"||{d}^\n")
            print(f"✅ combined_part2.txt erstellt ({len(part2)} Domains).")
        else:
            # Falls die Liste kleiner als 1,2 Mio ist, bleibt Part 2 leer
            open("combined_part2.txt", 'w').close()
            print("⚪ combined_part2.txt ist leer (Limit nicht erreicht).")

        # Optional: Die alte MASTER_FILE als Backup/Gesamtdatei behalten
        with open(MASTER_FILE, 'w', encoding='utf-8') as f:
            f.write("### TechRZN - MASTER BLOCKLIST (FULL) ###\n")
            f.write(f"### Total Unique Rules: {len(final_master)} ###\n\n")
            for d in final_master:
                f.write(f"||{d}^\n")
        
        print(f"\n✨ MASTER-BUILD FERTIG: Insgesamt {len(final_master)} Regeln verteilt.")
    else:
        print("\n❌ Fehler: Keine Domains für die Master-Liste gefunden.")
