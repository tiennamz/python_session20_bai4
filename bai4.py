import logging

logging.basicConfig(
    filename=r"C:\Users\ghast\OneDrive\Tài liệu\[IT205-K25] Lập trình ứng dụng với Python\session20\roster_app.log",
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s"
)

roster = [
    {
        "player_id": "P01",
        "name": "Faker",
        "role": "Mid Lane",
        "salary": 5000.0,
        "status": "Active"
    },
    {
        "player_id": "P02",
        "name": "Oner",
        "role": "Jungle",
        "salary": 3500.0,
        "status": "Active"
    },
    {
        "player_id": "P03",
        "name": "Ruler",
        "role": "ADC",
        "salary": 6000.0,
        "status": "Benched"
    }
]


def find_player_index(player_id, roster_list):
    for index, player in enumerate(roster_list):
        if player["player_id"] == player_id:
            return index
    return -1


def display_roster(roster_list):
    if not roster_list:
        print("Đội hình hiện đang trống.")
        return

    print("\n--- ĐỘI HÌNH RIKKEI ESPORTS ---")
    print(f"{'ID':<8}| {'Tên tuyển thủ':<20}| {'Vị trí':<15}| {'Lương':<12}| Trạng thái")
    print("-" * 85)

    for player in roster_list:
        player["name_display"] = player["name"]
        if player["status"] == "Benched":
            player["name_display"] += " [DỰ BỊ]"

        print("{player_id:<8}| {name_display:<20}| {role:<15}| {salary:<12,.1f}| {status}".format_map(player))

    logging.info("Coach viewed the team roster.")


def sign_player(roster_list):
    print("--- CHIÊU MỘ TUYỂN THỦ MỚI ---")

    player_id = input("Nhập mã tuyển thủ: ").strip().upper()

    if find_player_index(player_id, roster_list) != -1:
        print(f"Lỗi: Mã tuyển thủ {player_id} đã tồn tại.")
        logging.warning(f"Failed to sign player - Duplicate player ID {player_id}")
        return

    name = input("Nhập tên tuyển thủ: ").strip().title()
    role = input("Nhập vị trí thi đấu: ").strip().title()

    while True:
        try:
            salary = float(input("Nhập mức lương hàng tháng: "))

            if salary <= 0:
                print("Lương phải là số dương. Vui lòng nhập lại.")
                continue

            break

        except ValueError:
            print("Lương phải là số. Vui lòng nhập lại.")
            logging.warning(
                "Failed to sign player - Invalid salary input"
            )

    roster_list.append({
        "player_id": player_id,
        "name": name,
        "role": role,
        "salary": salary,
        "status": "Active"
    })

    print(f"\nThành công: Đã chiêu mộ tuyển thủ {name}.")
    logging.info(f"Signed new player {name} with salary {salary}")


def update_player_status(roster_list):
    print("\n--- CẬP NHẬT LƯƠNG & TRẠNG THÁI THI ĐẤU ---")

    player_id = input("Nhập mã tuyển thủ cần cập nhật: ").strip().upper()

    index = find_player_index(player_id, roster_list)

    if index == -1:
        print(f"Không tìm thấy tuyển thủ mang mã {player_id}.")
        logging.warning(f"Failed to update player - Player ID {player_id} not found")
        return

    player = roster_list[index]

    print(f"\nTuyển thủ: {player['name']}")
    print(f"Vị trí: {player['role']}")
    print(f"Lương hiện tại: {player['salary']:,.1f}")
    print(f"Trạng thái hiện tại: {player['status']}")

    print("""
1. Cập nhật lương
2. Cập nhật trạng thái thi đấu
""")

    choice = input("Chọn chức năng cập nhật (1-2): ")

    if choice == "1":

        old_salary = player["salary"]

        while True:
            try:
                new_salary = float(
                    input("Nhập mức lương mới: ")
                )

                if new_salary <= 0:
                    print("Lương phải lớn hơn 0.")
                    continue

                break

            except ValueError:
                print("Lương phải là số.")

        player["salary"] = new_salary

        print(f"Thành công: Đã cập nhật lương cho tuyển thủ {player_id}.")

        logging.info(
            f"Updated player {player_id} salary "
            f"from {old_salary} to {new_salary}"
        )

    elif choice == "2":

        print("""
1. Active
2. Benched
""")

        status_choice = input("Nhập lựa chọn trạng thái (1-2): ")

        old_status = player["status"]

        if status_choice == "1":
            player["status"] = "Active"

        elif status_choice == "2":
            player["status"] = "Benched"

        else:
            print("Lựa chọn không hợp lệ.")
            return

        print(f"Thành công: Đã cập nhật trạng thái cho tuyển thủ {player_id}.")

        logging.info(
            f"Updated player {player_id} status "
            f"from {old_status} to {player['status']}"
        )

    else:
        print("Lựa chọn không hợp lệ.")


def generate_payroll_report(roster_list):
    print("\n--- BÁO CÁO QUỸ LƯƠNG HÀNG THÁNG ---")

    if not roster_list:
        print("Đội hình hiện đang trống. Tổng quỹ lương: 0.0")
        return

    total_payroll = 0

    print(f"{'ID':<8}| {'Tên tuyển thủ':<15}| {'Trạng thái':<10}| {'Lương gốc':<12}| Lương thực nhận")
    print("-" * 85)

    try:
        for player in roster_list:

            salary = player["salary"]

            if player["status"] == "Benched":
                actual_salary = salary * 0.5
            else:
                actual_salary = salary

            total_payroll += actual_salary

            print(
                f"{player['player_id']:<8}| "
                f"{player['name']:<15}| "
                f"{player['status']:<10}| "
                f"{salary:<12,.1f}| "
                f"{actual_salary:,.1f}"
            )

    except KeyError as e:
        print("Lỗi: Một tuyển thủ đang bị thiếu dữ liệu.")
        logging.error(
            f"Missing key while generating payroll report: {e}"
        )
        total_payroll = 0

    print("-" * 85)
    print(f"Tổng quỹ lương hàng tháng: {total_payroll:,.1f}")

    logging.info(
        f"Generated monthly payroll report. Total: {total_payroll}"
    )


def main():
    while True:
        choice = input("""
===== HỆ THỐNG QUẢN LÝ ĐỘI HÌNH RIKKEI ESPORTS =====
1. Xem đội hình thi đấu hiện tại
2. Chiêu mộ tuyển thủ mới
3. Cập nhật lương & Trạng thái thi đấu
4. Báo cáo quỹ lương hàng tháng
5. Thoát hệ thống
==================================================
Chọn chức năng (1-5): """)

        if not choice.isdigit():
            print("Vui lòng nhập số nguyên.")
            continue

        choice = int(choice)

        match choice:
            case 1:
                display_roster(roster)

            case 2:
                sign_player(roster)

            case 3:
                update_player_status(roster)

            case 4:
                generate_payroll_report(roster)

            case 5:
                print("Thoát hệ thống.")
                logging.info("System shutdown.")
                break

            case _:
                print("Lựa chọn không hợp lệ.")
                logging.warning("Invalid menu choice selected")


main()