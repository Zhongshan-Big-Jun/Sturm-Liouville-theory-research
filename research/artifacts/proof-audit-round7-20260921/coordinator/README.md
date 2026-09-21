# Coordinator validation records

These are the exact implementations used to check preservation, reviewed sources, new links, the candidate manifest, real staged/committed Git blobs and final remote heads. They retain the local paths and baseline for this specific round. They are evidence of the validation method, not general maintenance entry points or permission to bypass the project gateway. Some require mutable local receipts, a particular pre-commit state, or remote state, so do not blindly rerun them after later development.

The final document-check, staged-object check and post-push DELIVERY.json are outside the repository to avoid self-referential commit hashes. This archive is finalized before publication-manifest.json. Protection and current default retrieval have separate published results. The source diff check excludes the six unrelated original dirty files and does not whitespace-normalize immutable evidence.
