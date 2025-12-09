**THA Project Root Structure (14 docs):**

├── CLAUDE.md              # Main AI guide

├── README.md              # Project overview

├── llm\_handover.md        # LLM handover state

├── QUICK\_START.md         # 5-min setup

├── QUICK\_TEST.md          # Quick testing

├── DEPLOYMENT.md          # Deployment guide

├── DOCKER\_SETUP\_GUIDE.md  # Docker setup (consolidated)

├── DOCKER\_TROUBLESHOOTING.md

├── TESTING\_GUIDE.md       # Testing (consolidated)

├── TESTING\_CHECKLIST.md   # Structured checklist

├── TESTING\_WITHOUT\_DOCKER.md

├── NEXT\_STEPS.md          # Roadmap

├── CONTRIBUTING.md        # Plugin contributions

├── SKYWIND-PLUGIN-MARKETPLACE-STRUCTURE.md

└── current\_ui\_application\_state.png  # Only screenshot kept

---

**Analysis Rules Structure (docs/th-context/analysis-rules/):**

├── ALERT\_CLASSIFICATION\_PRINCIPLES.md  # Core principle: severity is context-dependent

├── QUANTITATIVE\_ALERT\_WORKFLOW.md      # Step-by-step workflow for quantitative alerts

└── templates/
    └── quantitative-alert.yaml          # Template definition for quantitative reports

---

**Analysis Output (docs/analysis/):**

├── SD\_Negative\_Profit\_Deal\_Analysis.md

├── FI\_Comparison\_Monthly\_Purchase\_Volume\_Analysis.md

├── FI\_Exceptional\_Posting\_GL\_Account\_Analysis.md

├── PUR\_PREQ\_PO\_Value\_Check\_Analysis.md

├── MD\_Modified\_Vendor\_Bank\_Account\_Analysis.md

├── MD\_Modified\_Vendor\_Bank\_Account\_Repetitive\_Analysis.md  # With temporal sequencing

├── MM\_Material\_Moving\_Average\_Price\_Change\_Analysis.md     # Pure 4-artifact analysis

├── MM\_Material\_Standard\_Price\_Change\_Analysis.md           # 45K records, data quality focus

├── MM\_Inventory\_Count\_Plant\_Level\_Analysis.md              # Ghost inventory detection

├── SD\_Billing\_Document\_Status\_Analysis.md                   # Credit memo to one-time customer pattern

├── SD\_Payment\_Terms\_Check\_Analysis.md                       # Payment term override detection

└── SD\_Sales\_Orders\_1M\_Net\_Value\_Analysis.md                 # High-value orders validation ($28.9M)

