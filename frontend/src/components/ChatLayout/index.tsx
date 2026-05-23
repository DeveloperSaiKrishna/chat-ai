import styles from "./styles.module.css"

const ChatLayout = () => {
    return (
        <div className={styles.chatLayoutWrapper}>
            <div className={styles.docsSection}>
                <h2>Documents</h2>
            </div>
            <div className={styles.chatSection}>
                <h2>Documents</h2>
            </div>
            <div className={styles.modelsSection}>
                <h2>Documents</h2>
            </div>
        </div>
    )
}

export default ChatLayout