def count_word_frequency(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()


        for char in ".,!?;:'\"()-":
            text = text.replace(char, "")


        words = text.lower().split()


        word_counts = {}
        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1


        for word, count in word_counts.items():
            print(f"{word}: {count}")


    except FileNotFoundError:
        print("Error: The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
       
count_word_frequency("C:/Users/5308-2/Desktop/New folder/hello.txt")
