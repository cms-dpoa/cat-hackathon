# Inputs and Outputs

One type of input or output is a **Parameter**. Unlike artifacts, these are plain string values, and are useful for most simple cases.

**Artifacts** is a fancy name for a file that is compressed and stored in object storage (S3, MinIO, GCS, etc.).
 
## Let's recap:

-   There are two types of input and output: **parameters** and **artifacts**.
-   **Parameters** are just short strings.
-   **Artifacts** are simply files or directories that are compressed and uploaded to an **artifact repository** such as S3.
-   For one task to use the output of another task, declare a dependency using a DAG template or steps template.

Learn more about artifact features in the Argo Workflows documentation:

-   [Artifacts overview](https://argoproj.github.io/argo-workflows/walk-through/artifacts/)
-   [Configuring an artifact repository](https://argoproj.github.io/argo-workflows/configure-artifact-repository/)
-   [Key-only artifacts](https://argoproj.github.io/argo-workflows/key-only-artifacts/)
-   [Referencing artifact repositories](https://argoproj.github.io/argo-workflows/artifact-repository-ref/)