DROP TABLE IF EXISTS dialogue_records;
CREATE TABLE dialogue_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    input_text TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);

CREATE INDEX idx_user_session ON dialogue_records(user_id, session_id);
CREATE INDEX idx_timestamp ON dialogue_records(timestamp);