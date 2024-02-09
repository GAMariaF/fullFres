

def main():
    # Only prints some info

    print("""
    Variantbrowser Version: 0.1.1
          
    Commandline tools:
          
    vb-removesample: Delete a sample from the variant database.
          
    vb-unlocksample: Unlock a locked sample. It is sent back to the initial interpretation stage.
          
    vb-adduser: Add a new user to user database.
          
    vb-changepwd: Change password for a user. Existing password not needed.
          
    vb-generatedbs: Generate empty variant and user databases. Does not overwrite existing dbs.
          
    vb-backend: Run backend for development
    
    """)
    exit()


if __name__ == '__main__':
    main()