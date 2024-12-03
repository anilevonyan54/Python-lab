def analyze_log_file(input_file, output_file):
    try:
        status_code_counts = {200: 0, 404: 0, 500: 0}
        ip_counts = {}

        with open(input_file, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) < 6:
                    continue

                ip_address = parts[0]
                try:
                    status_code = int(parts[-2])
                except ValueError:
                    continue

                if status_code in status_code_counts:
                    status_code_counts[status_code] += 1

                if ip_address in ip_counts:
                    ip_counts[ip_address] += 1
                else:
                    ip_counts[ip_address] = 1

        most_common_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        with open(output_file, 'w') as out_file:
            out_file.write("Log Analysis Results\n")
            out_file.write("Total number of requests: {}\n".format(sum(status_code_counts.values())))
            out_file.write("Requests by status code:\n")
            for code, count in status_code_counts.items():
                out_file.write(f"{code}: {count}\n")
            out_file.write("Top 3 most common IP addresses:\n")
            for ip, count in most_common_ips:
                out_file.write(f"{ip}: {count}\n")

        print("Analysis complete. Results written to", output_file)

    except FileNotFoundError:
        print("Error: The input file was not found.")
    except IOError:
        print("Error: There was an issue reading or writing to the file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

analyze_log_file('input.log', 'output.txt')
