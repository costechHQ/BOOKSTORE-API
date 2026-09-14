

```mermaid
graph TD
    %% Styling Definitions
    classDef client fill:#EBF8FF,stroke:#3182CE,stroke-width:2px,color:#2B6CB0;
    classDef app fill:#EDF2F7,stroke:#4A5568,stroke-width:2px,color:#1A202C;
    classDef db fill:#FEFCBF,stroke:#D69E2E,stroke-width:2px,color:#744210;

    %% Client Layer
    subgraph Client_Layer ["Client Layer"]
        Client["Client<br/>(Swagger UI / Web Browser)"]:::client
    end

    %% Application Layer
    subgraph Application_Layer ["Application & Service Layer"]
        FastAPI["FastAPI Application<br/>• /authors<br/>• /books<br/>• Authentication"]:::app
        Alembic["Alembic<br/>(Database Migrations)"]:::app
    end

    %% Data Storage Layer
    subgraph Data_Layer ["Data Layer (PostgreSQL)"]
        DBSession["Database Session / ORM"]:::db
        PostgreSQL[("PostgreSQL Database<br/>• authors<br/>• books")]:::db
    end

    %% Infrastructure Containerization Boundary
    subgraph Docker_Compose ["Docker Compose Environment"]
        FastAPIContainer["FastAPI Container"]
        PostgresContainer["PostgreSQL Container"]
        FastAPIContainer -->|Connects to| PostgresContainer
    end

    %% Primary Data Flow Relationships
    Client -->|HTTP Requests| FastAPI
    FastAPI -->|Manages| DBSession
    DBSession -->|Queries / Persists| PostgreSQL
    Alembic -->|Applies Schema Changes| PostgreSQL

    %% Subgraph Styles
    style Client_Layer fill:none,stroke:none
    style Application_Layer fill:none,stroke:none
    style Data_Layer fill:none,stroke:none
    style Docker_Compose fill:#F7FAFC,stroke:#A0AEC0,stroke-width:1.5px,stroke-dasharray: 4 4
