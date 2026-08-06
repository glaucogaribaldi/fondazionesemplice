---
name: install-fondazionesemplice
description: Rebuild a dedicated Ubuntu NVIDIA VM from the fondazionesemplice GitHub repository, erase its existing Docker workloads without backup, enforce paper-only defaults, start the GPU stack, and verify health. Use only when the operator explicitly requests a destructive Fondazione VM reinstall.
---

# Install Fondazione Semplice

Use this only on the dedicated trading VM. Never run it on a shared host.

1. Ask for the exact GitHub repository URL and immutable tag or commit.
2. Confirm the target is the dedicated `g2-standard-8` VM and that no backup is wanted.
3. Explain that the script erases Docker workloads and `/opt/fondazionesemplice`; a true boot-disk format requires deleting and recreating the VM in GCP.
4. Require the operator to type `ERASE_FOUNDATION_VM_WITHOUT_BACKUP` exactly.
5. Clone the repository to a temporary directory and inspect `scripts/install_vm.sh` before execution.
6. Run:

   `sudo ./scripts/install_vm.sh --repo <trusted-url> --ref <tag-or-commit> --confirm ERASE_FOUNDATION_VM_WITHOUT_BACKUP`

7. Do not add Coinbase credentials during installation.
8. Verify `.env` contains `TRADING_MODE=paper`, `LIVE_ENABLED=false`, and an empty `LIVE_CONFIRMATION`.
9. Run `docker compose ps`, `nvidia-smi`, and `./scripts/smoke_test.sh`.
10. Report the checked-out commit, container health, GPU visibility, local dashboard addresses, and any failure. Never silently retry by weakening a security control.

