# AWS Glue Data Pipeline Architecture Diagrams

## 🏗️ Overall Architecture Overview

```mermaid
graph TB
    subgraph "Pipeline Account (YOUR_PIPELINE_ACCOUNT_ID)"
        GH[GitHub Repositories]
        IP[Infrastructure Pipeline]
        AP[Application Pipeline]
    end
    
    subgraph "Development Account (YOUR_DEV_ACCOUNT_ID)"
        subgraph "Infrastructure Resources"
            S3I[S3 Input Bucket]
            S3O[S3 Output Bucket]
            S3A[S3 Assets Bucket]
            IAM[IAM Roles]
            GDB[Glue Database]
            LF[Lambda Trigger]
        end
        
        subgraph "Application Resources"
            GJ[Glue Jobs]
            FP[FileProcessor]
        end
    end
    
    subgraph "Production Account (YOUR_PROD_ACCOUNT_ID)"
        subgraph "Infrastructure Resources Prod"
            S3IP[S3 Input Bucket]
            S3OP[S3 Output Bucket]
            S3AP[S3 Assets Bucket]
            IAMP[IAM Roles]
            GDBP[Glue Database]
            LFP[Lambda Trigger]
        end
        
        subgraph "Application Resources Prod"
            GJP[Glue Jobs]
            FPP[FileProcessor]
        end
    end
    
    GH --> IP
    GH --> AP
    IP --> S3I
    IP --> S3O
    IP --> S3A
    IP --> IAM
    IP --> GDB
    IP --> LF
    IP --> S3IP
    IP --> S3OP
    IP --> S3AP
    IP --> IAMP
    IP --> GDBP
    IP --> LFP
    
    AP --> GJ
    AP --> FP
    AP --> GJP
    AP --> FPP
    
    IAM -.-> GJ
    IAM -.-> FP
    IAMP -.-> GJP
    IAMP -.-> FPP
```

## 🔄 CI/CD Pipeline Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant IP as Infrastructure Pipeline
    participant AP as Application Pipeline
    participant DevEnv as Dev Environment
    participant ProdEnv as Prod Environment
    
    Dev->>GH: git push (infrastructure changes)
    GH->>IP: Webhook trigger
    IP->>IP: Build & Test
    IP->>DevEnv: Deploy infrastructure
    IP->>ProdEnv: Deploy infrastructure (with approval)
    
    Dev->>GH: git push (application changes)
    GH->>AP: Webhook trigger
    AP->>AP: Build & Test
    AP->>DevEnv: Deploy Glue jobs
    AP->>ProdEnv: Deploy Glue jobs (with approval)
    
    Note over DevEnv,ProdEnv: Cross-stack dependencies resolved via CloudFormation exports
```

## 📊 Data Processing Flow

```mermaid
graph LR
    subgraph "Data Processing Pipeline"
        CSV[CSV File Upload]
        S3[S3 Input Bucket]
        LT[Lambda Trigger]
        GJ[Glue Job]
        PROC[Data Processing]
        PAR[Parquet Output]
        S3O[S3 Output Bucket]
    end
    
    CSV --> S3
    S3 --> LT
    LT --> GJ
    GJ --> PROC
    PROC --> PAR
    PAR --> S3O
    
    subgraph "Processing Details"
        PROC --> SI[Schema Inference]
        PROC --> DT[Data Transformation]
        PROC --> ME[Metadata Enrichment]
        SI --> DT
        DT --> ME
    end
```

## 🏢 Multi-Account Architecture

```mermaid
graph TB
    subgraph "Pipeline Account"
        subgraph "Infrastructure Pipeline"
            IPS[Source: GitHub]
            IPB[Build: CDK Synth]
            IPD[Deploy: CloudFormation]
        end
        
        subgraph "Application Pipeline"
            APS[Source: GitHub]
            APB[Build: CDK Synth]
            APD[Deploy: CloudFormation]
        end
    end
    
    subgraph "Development Account"
        subgraph "Infrastructure Stack"
            IS3[S3 Buckets]
            IIAM[IAM Roles]
            ILF[Lambda Functions]
            IGD[Glue Database]
        end
        
        subgraph "Application Stack"
            AGJ[Glue Jobs]
            AJS[Job Scripts]
        end
        
        IS3 -.->|Exports| AGJ
        IIAM -.->|Exports| AGJ
        IGD -.->|Exports| AGJ
    end
    
    subgraph "Production Account"
        subgraph "Infrastructure Stack Prod"
            PS3[S3 Buckets]
            PIAM[IAM Roles]
            PLF[Lambda Functions]
            PGD[Glue Database]
        end
        
        subgraph "Application Stack Prod"
            PGJ[Glue Jobs]
            PJS[Job Scripts]
        end
        
        PS3 -.->|Exports| PGJ
        PIAM -.->|Exports| PGJ
        PGD -.->|Exports| PGJ
    end
    
    IPD --> IS3
    IPD --> IIAM
    IPD --> ILF
    IPD --> IGD
    IPD --> PS3
    IPD --> PIAM
    IPD --> PLF
    IPD --> PGD
    
    APD --> AGJ
    APD --> AJS
    APD --> PGJ
    APD --> PJS
```

## 🔐 Security & IAM Architecture

```mermaid
graph TB
    subgraph "Pipeline Account"
        PA[Pipeline Execution Role]
        CA[Cross-Account Roles]
    end
    
    subgraph "Development Account"
        subgraph "IAM Roles"
            GSR[Glue Service Role]
            LER[Lambda Execution Role]
            CAR[Cross-Account Role]
        end
        
        subgraph "Resources"
            S3B[S3 Buckets]
            GJ[Glue Jobs]
            LF[Lambda Functions]
        end
    end
    
    subgraph "Production Account"
        subgraph "IAM Roles Prod"
            GSRP[Glue Service Role]
            LERP[Lambda Execution Role]
            CARP[Cross-Account Role]
        end
        
        subgraph "Resources Prod"
            S3BP[S3 Buckets]
            GJP[Glue Jobs]
            LFP[Lambda Functions]
        end
    end
    
    PA --> CAR
    PA --> CARP
    CAR --> GSR
    CAR --> LER
    CARP --> GSRP
    CARP --> LERP
    
    GSR --> S3B
    GSR --> GJ
    LER --> LF
    LER --> GJ
    
    GSRP --> S3BP
    GSRP --> GJP
    LERP --> LFP
    LERP --> GJP
```

## 📈 Data Transformation Detail

```mermaid
graph LR
    subgraph "Input Processing"
        CSV[CSV File]
        UP[File Upload]
        S3I[S3 Input Bucket]
    end
    
    subgraph "Event Processing"
        S3E[S3 Event]
        LT[Lambda Trigger]
        GJS[Glue Job Start]
    end
    
    subgraph "Data Processing"
        READ[Read CSV]
        INFER[Infer Schema]
        TRANS[Transform Data]
        META[Add Metadata]
        WRITE[Write Parquet]
    end
    
    subgraph "Output"
        S3O[S3 Output Bucket]
        PAR[Parquet Files]
    end
    
    CSV --> UP
    UP --> S3I
    S3I --> S3E
    S3E --> LT
    LT --> GJS
    GJS --> READ
    READ --> INFER
    INFER --> TRANS
    TRANS --> META
    META --> WRITE
    WRITE --> S3O
    S3O --> PAR
    
    subgraph "Metadata Added"
        PT[processed_at]
        SF[source_file]
        PJ[processing_job]
    end
    
    META --> PT
    META --> SF
    META --> PJ
```

## 🔄 Repository Organization

```mermaid
graph TB
    subgraph "Infrastructure Repository"
        subgraph "CDK Stacks"
            IS[Infrastructure Stack]
            PS[Pipeline Stack]
            DS[Deployment Stage]
        end
        
        subgraph "Resources Defined"
            S3[S3 Buckets]
            IAM[IAM Roles]
            LF[Lambda Functions]
            GD[Glue Database]
        end
        
        IS --> S3
        IS --> IAM
        IS --> LF
        IS --> GD
    end
    
    subgraph "Application Repository"
        subgraph "CDK Stacks"
            AS[Application Stack]
            APS[App Pipeline Stack]
            AGS[App Glue Stage]
        end
        
        subgraph "Resources Defined"
            GJ[Glue Jobs]
            JS[Job Scripts]
        end
        
        subgraph "Job Scripts"
            FP[file_processor.py]
        end
        
        AS --> GJ
        AS --> JS
        JS --> FP
    end
    
    subgraph "Cross-Stack Dependencies"
        EX[CloudFormation Exports]
        IM[CloudFormation Imports]
    end
    
    IS --> EX
    EX --> IM
    IM --> AS
```

## 🚀 Deployment Pipeline Stages

```mermaid
graph LR
    subgraph "Infrastructure Pipeline"
        IS[Source]
        IB[Build]
        IU[Update Pipeline]
        ID[Deploy Dev]
        IMA[Manual Approval]
        IP[Deploy Prod]
        
        IS --> IB
        IB --> IU
        IU --> ID
        ID --> IMA
        IMA --> IP
    end
    
    subgraph "Application Pipeline"
        AS[Source]
        AB[Build]
        AU[Update Pipeline]
        AA[Assets]
        AD[Deploy Dev]
        AMA[Manual Approval]
        AP[Deploy Prod]
        
        AS --> AB
        AB --> AU
        AU --> AA
        AA --> AD
        AD --> AMA
        AMA --> AP
    end
    
    subgraph "Deployment Dependencies"
        ID -.->|Exports Available| AD
        IP -.->|Exports Available| AP
    end
```

## 📊 Monitoring & Observability

```mermaid
graph TB
    subgraph "Data Processing Events"
        FU[File Upload]
        LT[Lambda Trigger]
        GJ[Glue Job]
        JC[Job Complete]
    end
    
    subgraph "Monitoring Systems"
        CW[CloudWatch Logs]
        CWM[CloudWatch Metrics]
        S3E[S3 Events]
    end
    
    subgraph "Log Groups"
        LL[Lambda Logs]
        GL[Glue Job Logs]
        GE[Glue Error Logs]
    end
    
    FU --> S3E
    LT --> LL
    GJ --> GL
    GJ --> GE
    JC --> CWM
    
    LL --> CW
    GL --> CW
    GE --> CW
    S3E --> CW
    
    subgraph "Alerting"
        AL[CloudWatch Alarms]
        SNS[SNS Notifications]
    end
    
    CWM --> AL
    AL --> SNS
```

---

## 🎯 Key Architecture Benefits

### 1. **Separation of Concerns**
- Infrastructure and application code in separate repositories
- Independent deployment cycles
- Clear ownership boundaries

### 2. **GitOps Workflow**
- All changes tracked in Git
- Automated deployment from commits
- Rollback capability through Git history

### 3. **Multi-Account Security**
- Production isolation
- Least privilege access
- Cross-account role assumption

### 4. **Event-Driven Processing**
- Real-time file processing
- Automatic scaling
- No manual intervention required

### 5. **Observability**
- Comprehensive logging
- Metrics and monitoring
- Error tracking and alerting

---

## 💡 Tips for Better Diagram Viewing

Since Mermaid diagrams in Markdown can appear small, here are some tips:

1. **Browser Zoom**: Use Ctrl/Cmd + Plus to zoom in on the entire page
2. **Copy to Mermaid Live**: Copy any diagram code and paste it into [mermaid.live](https://mermaid.live) for full-screen viewing
3. **VS Code Extension**: Use the Mermaid Preview extension in VS Code for better rendering
4. **Export Options**: Most Mermaid viewers allow exporting to PNG/SVG for presentations

*These diagrams provide a complete visual representation of the enterprise data pipeline architecture, suitable for technical presentations and documentation.*