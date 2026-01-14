import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymysql
from datetime import datetime
from PIL import Image, ImageTk

class HospitalManagementSystem:
    def open_visit_window(self):
        """打开就诊管理窗口"""
        visit_window = tk.Toplevel(self.root)
        visit_window.title("就诊管理")
        visit_window.geometry("1000x600")

        columns_list = self.get_select_columns_list('Visit')
        columns = tuple(columns_list)
        visit_tree = ttk.Treeview(visit_window, columns=columns, show="headings", height=20)

        for col in columns:
            visit_tree.heading(col, text=col)
            visit_tree.column(col, width=120)

        visit_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(visit_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=lambda: self.refresh_tree_data(visit_tree, "Visit")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=lambda: self.open_add_visit_window(visit_tree)).pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(btn_frame, text="编辑", command=lambda: self.open_edit_visit_window(visit_tree)).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=lambda: self.open_delete_visit_window(visit_tree)).pack(side=tk.LEFT,
                                                                                                           padx=5)
        # 添加就诊单按钮
        ttk.Button(btn_frame, text="填写就诊单", command=lambda: self.open_visit_form_window(visit_tree)).pack(
            side=tk.LEFT, padx=5)

        # 加载数据
        self.refresh_tree_data(visit_tree, "Visit")

    def open_visit_form_window(self, visit_tree):
        """打开就诊单填写窗口"""
        selected = visit_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择一个就诊记录来填写就诊单")
            return

        item = visit_tree.item(selected[0])
        visit_id = item['values'][0]  # 假设visit_id是第一列

        # 检查是否已存在费用记录
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Charge WHERE visit_id = %s", (visit_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                if not messagebox.askyesno("确认", f"该就诊记录（ID: {visit_id}）已存在费用信息，是否要更新现有记录？"):
                    return

        # 创建就诊单窗口
        form_window = tk.Toplevel(self.root)
        form_window.title("填写就诊单")
        form_window.geometry("700x600")

        # 获取就诊记录的详细信息
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT v.visit_id, v.patient_id, p.full_name as patient_name, v.doctor_id, s.staff_name as doctor_name, 
                       v.checkin_time, v.diagnosis, v.prescription
                FROM Visit v
                JOIN Patient p ON v.patient_id = p.patient_id
                JOIN Staff s ON v.doctor_id = s.staff_id
                WHERE v.visit_id = %s
            """, (visit_id,))
            visit_data = cursor.fetchone()

        if not visit_data:
            messagebox.showerror("错误", "未找到对应的就诊记录")
            return

        # 显示就诊信息
        ttk.Label(form_window, text="就诊ID:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, padx=10,
                                                                                pady=5)
        ttk.Label(form_window, text=str(visit_data[0])).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        ttk.Label(form_window, text="患者姓名:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky=tk.W, padx=10,
                                                                                  pady=5)
        ttk.Label(form_window, text=visit_data[2]).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        ttk.Label(form_window, text="医生姓名:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=tk.W, padx=10,
                                                                                  pady=5)
        ttk.Label(form_window, text=visit_data[4]).grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        # 费用项目输入
        ttk.Label(form_window, text="诊疗费:", font=("Arial", 12)).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        consultation_fee = ttk.Entry(form_window, width=20)
        consultation_fee.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(form_window, text="药品费:", font=("Arial", 12)).grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        medicine_fee = ttk.Entry(form_window, width=20)
        medicine_fee.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(form_window, text="检查费:", font=("Arial", 12)).grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        test_fee = ttk.Entry(form_window, width=20)
        test_fee.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(form_window, text="其他费用:", font=("Arial", 12)).grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        other_fee = ttk.Entry(form_window, width=20)
        other_fee.grid(row=6, column=1, padx=10, pady=5)

        ttk.Label(form_window, text="保险报销:", font=("Arial", 12)).grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)
        insurance_covered = ttk.Entry(form_window, width=20)
        insurance_covered.grid(row=7, column=1, padx=10, pady=5)

        ttk.Label(form_window, text="支付方式:", font=("Arial", 12)).grid(row=8, column=0, sticky=tk.W, padx=10, pady=5)
        payment_method = ttk.Combobox(form_window, values=["Cash", "Card", "Insurance", "WeChat", "Alipay"], width=17)
        payment_method.grid(row=8, column=1, padx=10, pady=5)
        payment_method.set("现金")

        ttk.Label(form_window, text="支付状态:", font=("Arial", 12)).grid(row=9, column=0, sticky=tk.W, padx=10, pady=5)
        payment_status = ttk.Combobox(form_window, values=["Unpaid", "Paid", "InsurancePending"], width=17)
        payment_status.grid(row=9, column=1, padx=10, pady=5)
        payment_status.set("未支付")

        # 计算总费用和自付费用
        def calculate_fees(*args):
            try:
                # 获取输入值
                consult_fee = float(consultation_fee.get() or 0)
                med_fee = float(medicine_fee.get() or 0)
                test_fee_val = float(test_fee.get() or 0)
                other_fee_val = float(other_fee.get() or 0)
                insurance = float(insurance_covered.get() or 0)

                # 计算总费用
                total = consult_fee + med_fee + test_fee_val + other_fee_val
                self_pay = total - insurance

                # 更新显示
                total_amount.set(f"{total:.2f}")
                self_pay_amount.set(f"{self_pay:.2f}")
            except ValueError:
                # 如果输入无效，清空计算结果
                total_amount.set("0.00")
                self_pay_amount.set("0.00")

        # 绑定费用输入框的事件
        consultation_fee.bind('<KeyRelease>', calculate_fees)
        medicine_fee.bind('<KeyRelease>', calculate_fees)
        test_fee.bind('<KeyRelease>', calculate_fees)
        other_fee.bind('<KeyRelease>', calculate_fees)
        insurance_covered.bind('<KeyRelease>', calculate_fees)

        # 显示计算结果
        ttk.Label(form_window, text="总费用:", font=("Arial", 12, "bold")).grid(row=10, column=0, sticky=tk.W, padx=10,
                                                                                pady=5)
        total_amount = tk.StringVar(value="0.00")
        ttk.Label(form_window, textvariable=total_amount, font=("Arial", 12, "bold")).grid(row=10, column=1,
                                                                                           sticky=tk.W, padx=10, pady=5)

        ttk.Label(form_window, text="自付费用:", font=("Arial", 12, "bold")).grid(row=11, column=0, sticky=tk.W,
                                                                                  padx=10, pady=5)
        self_pay_amount = tk.StringVar(value="0.00")
        ttk.Label(form_window, textvariable=self_pay_amount, font=("Arial", 12, "bold")).grid(row=11, column=1,
                                                                                              sticky=tk.W, padx=10,
                                                                                              pady=5)

        # 保存就诊单
        def save_charge():
            try:
                with self.connection.cursor() as cursor:
                    # 检查是否已存在该visit_id的记录
                    cursor.execute("SELECT COUNT(*) FROM Charge WHERE visit_id = %s", (visit_id,))
                    count = cursor.fetchone()[0]

                    if count > 0:
                        # 如果已存在，执行更新操作
                        result = cursor.execute("""
                            UPDATE Charge 
                            SET consultation_fee=%s, medicine_fee=%s, test_fee=%s, other_fee=%s, 
                                insurance_covered=%s, payment_method=%s, payment_status=%s, 
                                total_amount=%s, self_pay=%s
                            WHERE visit_id = %s
                        """, (
                            float(consultation_fee.get() or 0),
                            float(medicine_fee.get() or 0),
                            float(test_fee.get() or 0),
                            float(other_fee.get() or 0),
                            float(insurance_covered.get() or 0),
                            payment_method.get(),
                            payment_status.get(),
                            float(total_amount.get()),
                            float(self_pay_amount.get()),
                            visit_id
                        ))

                        # 检查更新是否成功
                        if result == 0:
                            messagebox.showwarning("警告", f"未找到ID为 {visit_id} 的费用记录")
                            return
                    else:
                        # 如果不存在，执行插入操作
                        cursor.execute("""
                            INSERT INTO Charge (
                                visit_id, consultation_fee, medicine_fee, test_fee, other_fee, 
                                insurance_covered, payment_method, payment_status, total_amount, self_pay
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            visit_id,
                            float(consultation_fee.get() or 0),
                            float(medicine_fee.get() or 0),
                            float(test_fee.get() or 0),
                            float(other_fee.get() or 0),
                            float(insurance_covered.get() or 0),
                            payment_method.get(),
                            payment_status.get(),
                            float(total_amount.get()),
                            float(self_pay_amount.get())
                        ))

                    # 更新支付时间（如果已支付）
                    if payment_status.get() == "已支付":
                        cursor.execute("UPDATE Charge SET payment_time = NOW() WHERE visit_id = %s", (visit_id,))

                self.connection.commit()

                # 更新首页统计信息
                if hasattr(self, 'stats_frame'):
                    self.update_statistics(self.stats_frame)

                # 更新收入统计窗口（如果存在）
                try:
                    if hasattr(self, 'revenue_window') and self.revenue_window.winfo_exists():
                        # 刷新收入统计树形控件
                        if hasattr(self, 'revenue_tree'):
                            self.refresh_revenue_data(self.revenue_tree)
                except Exception:
                    pass

                # 更新详细收入信息窗口（如果存在）
                try:
                    if hasattr(self, 'detailed_window') and self.detailed_window.winfo_exists():
                        # 刷新详细收入树形控件
                        if hasattr(self, 'detailed_tree'):
                            self.refresh_detailed_revenue_data(self.detailed_tree)
                except Exception:
                    pass

                messagebox.showinfo("成功", "就诊单费用信息已保存")
                form_window.destroy()
            except ValueError as ve:
                messagebox.showerror("错误", f"输入值错误: 请检查费用输入是否为有效数字")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
        ttk.Button(form_window, text="保存", command=save_charge).grid(row=12, column=0, columnspan=2, sticky=tk.W,
                                                                      padx=10, pady=5)
    def open_add_visit_window(self, tree):
        """打开添加就诊窗口"""
        # 获取表的列信息
        with self.connection.cursor() as cursor:
            cursor.execute("DESCRIBE Visit")
            columns_info = cursor.fetchall()

        # 创建添加窗口
        add_window = tk.Toplevel(self.root)
        add_window.title("添加就诊记录")
        add_window.geometry("600x500")

        # 创建表单
        entries = {}
        row_idx = 0

        # 获取患者列表
        patient_list = self.get_patient_list()
        # 获取医生列表
        doctor_list = self.get_doctor_list()

        for col_info in columns_info:
            col_name = col_info[0]
            extra = col_info[5] or ''

            # 跳过自增主键
            if 'auto_increment' in extra:
                continue

            ttk.Label(add_window, text=f"{col_name}:").grid(row=row_idx, column=0, sticky=tk.W, padx=10, pady=5)

            if col_name == 'patient_id':
                # 患者选择下拉框
                patient_combo = ttk.Combobox(add_window, values=[f"{p[0]} - {p[1]}" for p in patient_list], width=30)
                patient_combo.grid(row=row_idx, column=1, padx=10, pady=5)
                entries[col_name] = patient_combo
            elif col_name == 'doctor_id':
                # 医生选择下拉框
                doctor_combo = ttk.Combobox(add_window, values=[f"{d[0]} - {d[1]}" for d in doctor_list], width=30)
                doctor_combo.grid(row=row_idx, column=1, padx=10, pady=5)
                entries[col_name] = doctor_combo
            elif col_name == 'checkin_time':
                # 日期时间输入
                datetime_entry = ttk.Entry(add_window, width=30)
                datetime_entry.grid(row=row_idx, column=1, padx=10, pady=5)
                datetime_entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                entries[col_name] = datetime_entry
            elif col_name in ['complaint', 'diagnosis', 'treatment_plan', 'prescription']:
                # 多行文本框
                text_widget = tk.Text(add_window, width=30, height=3)
                text_widget.grid(row=row_idx, column=1, padx=10, pady=5)
                entries[col_name] = text_widget
            else:
                entry = ttk.Entry(add_window, width=30)
                entry.grid(row=row_idx, column=1, padx=10, pady=5)
                entries[col_name] = entry

            row_idx += 1

        # 按钮
        def save_visit():
            try:
                with self.connection.cursor() as cursor:
                    # 构建INSERT语句
                    col_names = list(entries.keys())
                    placeholders = ['%s'] * len(col_names)

                    # 分离文本框和下拉框的值
                    values = []
                    for col_name, widget in entries.items():
                        if isinstance(widget, tk.Text):
                            # 文本框取值
                            value = widget.get("1.0", tk.END).strip()
                        elif isinstance(widget, ttk.Combobox):
                            # 下拉框取值，格式为 "ID - Name"，取ID部分
                            selected = widget.get()
                            if selected and ' - ' in selected:
                                value = selected.split(' - ')[0]
                            else:
                                value = selected
                        else:
                            # 普通输入框
                            value = widget.get()

                        values.append(value)

                    sql = f"INSERT INTO Visit ({', '.join(col_names)}) VALUES ({', '.join(placeholders)})"
                    cursor.execute(sql, values)
                self.connection.commit()
                # 将插入操作可撤销（删除插入的记录）
                try:
                    last_id = cursor.lastrowid
                    id_col = self.get_primary_key_column('Visit')
                    self.push_undo({'type': 'delete', 'table': 'Visit', 'id_column': id_col, 'id': last_id})
                except Exception:
                    pass
                messagebox.showinfo("成功", "就诊记录添加成功")
                add_window.destroy()
                self.refresh_tree_data(tree, "Visit", self.get_select_columns("Visit"))
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        # 保存按钮
        ttk.Button(add_window, text="保存", command=save_visit).grid(row=row_idx, column=0, columnspan=2, pady=10)

    def get_patient_list(self):
        """获取患者列表"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT patient_id, full_name FROM Patient ORDER BY patient_id")
            return cursor.fetchall()

    def get_doctor_list(self):
        """获取医生列表"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT staff_id, staff_name FROM Staff WHERE position = 'doctor' ORDER BY staff_id")
            return cursor.fetchall()

    def open_edit_visit_window(self, tree):
        """打开编辑就诊窗口"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要编辑的就诊记录")
            return

        item = tree.item(selected[0])
        visit_id = item['values'][0]

        # 获取表的列信息
        with self.connection.cursor() as cursor:
            cursor.execute("DESCRIBE Visit")
            columns_info = cursor.fetchall()
            col_names = [col[0] for col in columns_info]

        # 获取当前记录数据
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Visit WHERE visit_id = %s", (visit_id,))
            current_data = cursor.fetchone()

        # 创建编辑窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑就诊记录")
        edit_window.geometry("600x500")

        # 创建表单
        entries = {}
        row_idx = 0

        # 获取患者列表
        patient_list = self.get_patient_list()
        # 获取医生列表
        doctor_list = self.get_doctor_list()

        for col_info in columns_info:
            col_name = col_info[0]
            # 跳过主键
            if col_name == 'visit_id':
                continue

            ttk.Label(edit_window, text=f"{col_name}:").grid(row=row_idx, column=0, sticky=tk.W, padx=10, pady=5)

            # 获取当前值
            try:
                idx = col_names.index(col_name)
                val = current_data[idx] if current_data[idx] is not None else ""
            except Exception:
                val = ""

            if col_name == 'patient_id':
                # 患者选择下拉框
                patient_combo = ttk.Combobox(edit_window, values=[f"{p[0]} - {p[1]}" for p in patient_list], width=30)
                patient_combo.grid(row=row_idx, column=1, padx=10, pady=5)
                # 设置当前值
                if val:
                    current_patient = [p for p in patient_list if str(p[0]) == str(val)]
                    if current_patient:
                        patient_combo.set(f"{current_patient[0][0]} - {current_patient[0][1]}")
                entries[col_name] = patient_combo
            elif col_name == 'doctor_id':
                # 医生选择下拉框
                doctor_combo = ttk.Combobox(edit_window, values=[f"{d[0]} - {d[1]}" for d in doctor_list], width=30)
                doctor_combo.grid(row=row_idx, column=1, padx=10, pady=5)
                # 设置当前值
                if val:
                    current_doctor = [d for d in doctor_list if str(d[0]) == str(val)]
                    if current_doctor:
                        doctor_combo.set(f"{current_doctor[0][0]} - {current_doctor[0][1]}")
                entries[col_name] = doctor_combo
            elif col_name in ['complaint', 'diagnosis', 'treatment_plan', 'prescription']:
                # 多行文本框
                text_widget = tk.Text(edit_window, width=30, height=3)
                text_widget.grid(row=row_idx, column=1, padx=10, pady=5)
                text_widget.insert("1.0", str(val))
                entries[col_name] = text_widget
            else:
                entry = ttk.Entry(edit_window, width=30)
                entry.grid(row=row_idx, column=1, padx=10, pady=5)
                entry.insert(0, str(val))
                entries[col_name] = entry

            entries[col_name] = locals().get(col_name + '_combo', locals().get(col_name + '_widget',
                                                                               locals().get(col_name + '_entry',
                                                                                            locals().get(col_name))))
            row_idx += 1

        # 按钮
        def update_visit():
            try:
                # 备份旧数据以便撤销
                try:
                    old = None
                    with self.connection.cursor() as _c:
                        _c.execute("SELECT * FROM Visit WHERE visit_id = %s", (visit_id,))
                        row = _c.fetchone()
                        if row:
                            _c.execute("DESCRIBE Visit")
                            cols = [c[0] for c in _c.fetchall()]
                            old = dict(zip(cols, row))
                except Exception:
                    pass

                with self.connection.cursor() as cursor:
                    # 构建UPDATE语句
                    set_parts = []
                    values = []

                    for col_name, widget in entries.items():
                        if isinstance(widget, tk.Text):
                            # 文本框取值
                            value = widget.get("1.0", tk.END).strip()
                        elif isinstance(widget, ttk.Combobox):
                            # 下拉框取值
                            selected = widget.get()
                            if selected and ' - ' in selected:
                                value = selected.split(' - ')[0]
                            else:
                                value = selected
                        else:
                            # 普通输入框
                            value = widget.get()

                        set_parts.append(f"`{col_name}` = %s")
                        values.append(value)

                    sql = f"UPDATE Visit SET {', '.join(set_parts)} WHERE visit_id = %s"
                    values.append(visit_id)
                    cursor.execute(sql, values)
                self.connection.commit()
                messagebox.showinfo("成功", "就诊记录更新成功")
                edit_window.destroy()
                self.refresh_tree_data(tree, "Visit", self.get_select_columns("Visit"))
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {str(e)}")

        ttk.Button(edit_window, text="更新", command=update_visit).grid(row=row_idx, column=0, columnspan=2, pady=10)

    def open_delete_visit_window(self, tree):
        """打开删除就诊窗口"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要删除的就诊记录")
            return

        item = tree.item(selected[0])
        visit_id = item['values'][0]

        if messagebox.askyesno("确认", "确定要删除这个就诊记录吗？"):
            try:
                # 备份整行
                old = self.fetch_row_by_id('Visit', 'visit_id', visit_id)
                with self.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Visit WHERE visit_id = %s", (visit_id,))
                self.connection.commit()
                if old:
                    self.push_undo({'type': 'insert', 'table': 'Visit', 'data': old})
                messagebox.showinfo("成功", "就诊记录删除成功")
                self.refresh_tree_data(tree, "Visit", self.get_select_columns("Visit"))
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def __init__(self, root):
        self.root = root
        self.root.title("社区医院管理系统")
        self.root.geometry("1200x800")

        # 数据库连接配置
        self.connection = None
        self.connect_to_database()

        # 撤销栈（保存可逆操作，最新的在栈顶）
        # 每个操作为 dict: { 'type': 'insert'|'delete'|'update'|'bulk_restore', 'table':..., 'id_column':..., 'data':... }
        self.undo_stack = []
        self.max_undo = 50

        # 创建主界面
        self.create_main_interface()
        # 背景图片路径和 PhotoImage 引用
        self.bg_image_path = None
        self._bg_photo = None

    def connect_to_database(self):
        """连接到数据库"""
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='81357108Aa',  # 请修改为实际密码
                database='community_hospital_db_2',
                charset='utf8mb4'
            )
            print("数据库连接成功")
        except Exception as e:
            messagebox.showerror("错误", f"数据库连接失败: {str(e)}")

    def create_main_interface(self):
        """创建主界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 设置背景图片
        self.set_background_image(main_frame)

        # 创建菜单栏
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # 数据管理菜单
        data_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="数据管理", menu=data_menu)
        data_menu.add_command(label="科室管理", command=self.open_department_window)
        data_menu.add_command(label="员工管理", command=self.open_staff_window)
        data_menu.add_command(label="医生管理", command=self.open_doctor_window)
        data_menu.add_command(label="诊室管理", command=self.open_room_window)
        data_menu.add_command(label="患者管理", command=self.open_patient_window)
        data_menu.add_command(label="就诊管理", command=self.open_visit_window)
        # 撤销操作
        data_menu.add_separator()
        data_menu.add_command(label="撤销", command=self.undo_last_action)
        # 新增：清空所有数据操作
        data_menu.add_separator()
        data_menu.add_command(label="清空所有数据", command=self.clear_all_data)

        # 统计分析菜单
        analysis_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="统计分析", menu=analysis_menu)
        analysis_menu.add_command(label="收入统计", command=self.open_revenue_analysis)
        analysis_menu.add_command(label="预约统计", command=self.open_appointment_analysis)

        # 设置菜单
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="设置", menu=settings_menu)
        settings_menu.add_command(label="背景图片", command=self.choose_background_image)

        # 创建主标签页
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # 首页标签页
        home_frame = ttk.Frame(notebook)
        notebook.add(home_frame, text="首页")
        self.create_home_page(home_frame)

        # 科室管理标签页
        dept_frame = ttk.Frame(notebook)
        notebook.add(dept_frame, text="科室管理")
        self.create_department_page(dept_frame)

        # 员工管理标签页
        staff_frame = ttk.Frame(notebook)
        notebook.add(staff_frame, text="员工管理")
        self.create_staff_page(staff_frame)

        # 患者管理标签页
        patient_frame = ttk.Frame(notebook)
        notebook.add(patient_frame, text="患者管理")
        self.create_patient_page(patient_frame)

    def set_background_image(self, parent):
        """设置背景图片。若 self.bg_image_path 为 None 则不设置。支持窗口缩放自动适配。"""
        # 如果没有设置路径，不显示背景
        if not getattr(self, 'bg_image_path', None):
            return

        image_path = self.bg_image_path
        try:
            img = Image.open(image_path)
        except Exception as e:
            messagebox.showerror("错误", f"无法打开背景图片: {str(e)}")
            return

        # 获取目标大小（优先使用 parent 的当前大小）
        try:
            w = parent.winfo_width() or parent.winfo_reqwidth() or 1200
            h = parent.winfo_height() or parent.winfo_reqheight() or 800
        except Exception:
            w, h = 1200, 800

        try:
            resized = img.resize((max(1, w), max(1, h)), Image.Resampling.LANCZOS)
        except Exception:
            resized = img

        try:
            photo = ImageTk.PhotoImage(resized)
        except Exception as e:
            messagebox.showerror("错误", f"无法创建 PhotoImage: {e}")
            return

        # 如果已存在背景标签，更新图片；否则创建新的
        if hasattr(self, '_bg_label') and self._bg_label.winfo_exists():
            self._bg_label.configure(image=photo)
            self._bg_label.image = photo
        else:
            self._bg_label = tk.Label(parent, image=photo)
            self._bg_label.image = photo
            self._bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 保持引用，防止被垃圾回收
        self._bg_photo = photo

        # 在父容器大小改变时自动调整背景
        def _on_parent_resize(event):
            try:
                # reload original image to avoid repeated resampling from already resized image
                img2 = Image.open(image_path)
                resized2 = img2.resize((max(1, event.width), max(1, event.height)), Image.Resampling.LANCZOS)
                photo2 = ImageTk.PhotoImage(resized2)
                if hasattr(self, '_bg_label') and self._bg_label.winfo_exists():
                    self._bg_label.configure(image=photo2)
                    self._bg_label.image = photo2
                    self._bg_photo = photo2
            except Exception:
                pass

        # bind resize on the toplevel/root
        try:
            root_toplevel = self.root
            root_toplevel.bind('<Configure>', _on_parent_resize)
        except Exception:
            pass

    def choose_background_image(self):
        """弹出文件对话框让用户选择背景图片，并应用之"""
        filetypes = [('Image files', '*.png *.jpg *.jpeg *.bmp *.gif'), ('All files', '*.*')]
        path = filedialog.askopenfilename(title='选择背景图片', filetypes=filetypes)
        if not path:
            return
        self.bg_image_path = path
        # 尝试设置背景到主界面（stats_frame 的父容器即主框架已传入时，重-render）
        try:
            # find the main frame used earlier; we used local variable main_frame in create_main_interface,
            # not stored — instead set on root
            # attach bg to root directly
            self.set_background_image(self.root)
        except Exception:
            try:
                self.set_background_image(self.stats_frame)
            except Exception:
                pass

    # ---------------------- 撤销相关辅助方法 ----------------------
    def get_primary_key_column(self, table_name):
        """返回表的主键或自增字段名（优先找到 Key='PRI' 的列）"""
        with self.connection.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table_name}")
            cols = cursor.fetchall()
        # cols: (Field, Type, Null, Key, Default, Extra)
        for col in cols:
            if col[3] == 'PRI':
                return col[0]
        for col in cols:
            if 'auto_increment' in (col[5] or ''):
                return col[0]
        # fallback to first column
        return cols[0][0] if cols else None

    def fetch_row_by_id(self, table_name, id_column, record_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} WHERE {id_column} = %s", (record_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            # fetch column names
            cursor.execute(f"DESCRIBE {table_name}")
            col_info = cursor.fetchall()
            cols = [c[0] for c in col_info]
            return dict(zip(cols, row))

    def insert_row(self, table_name, row_dict):
        cols = list(row_dict.keys())
        placeholders = ', '.join(['%s'] * len(cols))
        cols_str = ', '.join([f"`{c}`" for c in cols])
        sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, [row_dict[c] for c in cols])
            return cursor.lastrowid

    def update_row_by_id(self, table_name, id_column, record_id, row_dict):
        set_clause = ', '.join([f"`{c}` = %s" for c in row_dict.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, list(row_dict.values()) + [record_id])

    def delete_row_by_id(self, table_name, id_column, record_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (record_id,))

    def push_undo(self, action):
        """推入撤销栈，并限制栈大小"""
        self.undo_stack.append(action)
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)

    def undo_last_action(self):
        """执行并弹出最近的一次可撤销操作"""
        if not self.undo_stack:
            messagebox.showinfo("撤销", "没有可撤销的操作")
            return
        action = self.undo_stack.pop()
        try:
            atype = action.get('type')
            if atype == 'delete':
                # 删除一条记录（用于撤销 insert）
                self.delete_row_by_id(action['table'], action['id_column'], action['id'])
            elif atype == 'insert':
                # 插入一条记录（用于撤销 delete）
                self.insert_row(action['table'], action['data'])
            elif atype == 'update':
                # 恢复到旧数据
                self.update_row_by_id(action['table'], action['id_column'], action['id'], action['data'])
            elif atype == 'bulk_restore':
                # 批量恢复：action['data'] = { table: [row_dict,...], ... }
                try:
                    # 关闭外键检查以便按任意顺序恢复数据
                    with self.connection.cursor() as _c:
                        _c.execute("SET FOREIGN_KEY_CHECKS=0;")
                    for t, rows in action['data'].items():
                        # 直接插入所有行
                        for row in rows:
                            try:
                                self.insert_row(t, row)
                            except Exception as e:
                                print(f"恢复表 {t} 的一行失败: {e}")
                finally:
                    try:
                        with self.connection.cursor() as _c:
                            _c.execute("SET FOREIGN_KEY_CHECKS=1;")
                    except Exception:
                        pass
            else:
                messagebox.showwarning("撤销", f"未知撤销类型: {atype}")
                return
            self.connection.commit()
            messagebox.showinfo("撤销", "已撤销最近一次操作")
            # 刷新界面
            try:
                if hasattr(self, 'refresh_department_data'):
                    self.refresh_department_data()
                if hasattr(self, 'refresh_staff_data'):
                    self.refresh_staff_data()
                if hasattr(self, 'refresh_patient_data'):
                    self.refresh_patient_data()
                if hasattr(self, 'stats_frame'):
                    self.update_statistics(self.stats_frame)
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror("撤销失败", f"撤销操作失败: {e}")

    def create_home_page(self, parent):
        """创建首页"""
        # 欢迎信息
        welcome_label = ttk.Label(parent, text="欢迎使用社区医院管理系统", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=20)

        # 系统统计信息
        self.stats_frame = ttk.Frame(parent)
        self.stats_frame.pack(fill=tk.X, padx=20, pady=10)

        # 显示统计数据
        self.update_statistics(self.stats_frame)

        # 操作按钮
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="刷新统计", command=lambda: self.update_statistics(self.stats_frame)).pack(
            side=tk.LEFT,
            padx=10)
        ttk.Button(btn_frame, text="预约管理", command=self.open_appointment_window).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="就诊管理", command=self.open_visit_window).pack(side=tk.LEFT, padx=10)

    def update_statistics(self, parent):
        """更新统计信息"""
        # 清空现有内容
        for widget in parent.winfo_children():
            widget.destroy()

        # 查询统计信息
        if self.connection:
            with self.connection.cursor() as cursor:
                # 科室数量
                cursor.execute("SELECT COUNT(*) FROM community_hospital_db_2.Department")
                dept_count = cursor.fetchone()[0]

                # 员工数量
                cursor.execute("SELECT COUNT(*) FROM community_hospital_db_2.Staff")
                staff_count = cursor.fetchone()[0]

                # 医生数量（查询 Staff 表中 position 为 'doctor' 的员工）
                cursor.execute("SELECT COUNT(*) FROM community_hospital_db_2.Staff WHERE position = 'doctor'")
                doctor_count = cursor.fetchone()[0]

                # 患者数量
                cursor.execute("SELECT COUNT(*) FROM community_hospital_db_2.Patient")
                patient_count = cursor.fetchone()[0]

                # 今日预约数
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute("SELECT COUNT(*) FROM community_hospital_db_2.Appointment WHERE appointment_date = %s",
                               (today,))
                today_appointments = cursor.fetchone()[0]

                # 今日就诊数
                cursor.execute("SELECT COUNT(*) FROM community_hospital_db_2.Visit WHERE DATE(checkin_time) = %s",
                               (today,))
                today_visits = cursor.fetchone()[0]

                # 今日收入
                cursor.execute("""
                    SELECT COALESCE(SUM(total_amount), 0) 
                    FROM Charge c 
                    JOIN Visit v ON c.visit_id = v.visit_id 
                    WHERE DATE(v.checkin_time) = %s
                """, (today,))
                today_revenue = cursor.fetchone()[0]

            # 显示统计信息
            stats_info = [
                ("科室数量", dept_count),
                ("员工数量", staff_count),
                ("医生数量", doctor_count),
                ("患者数量", patient_count),
                ("今日预约", today_appointments),
                ("今日就诊", today_visits),
                ("今日收入", f"¥{today_revenue:.2f}"),
                ("累计就诊", self.get_total_visits()),
                ("累计收入", f"¥{self.get_total_revenue():.2f}")
            ]

            for i, (label, value) in enumerate(stats_info):
                row = i // 3
                col = i % 3
                frame = ttk.Frame(parent)
                frame.grid(row=row, column=col, padx=10, pady=10)

                ttk.Label(frame, text=f"{label}:", font=("Arial", 12, "bold")).pack()
                ttk.Label(frame, text=str(value), font=("Arial", 14, "bold"), foreground="blue").pack()

    def get_total_visits(self):
        """获取累计就诊数"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Visit")
            return cursor.fetchone()[0]

    def get_total_revenue(self):
        """获取累计收入"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM Charge")
            return cursor.fetchone()[0]

    def get_total_visits(self):
        """获取累计就诊数"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Visit")
            return cursor.fetchone()[0]

    def get_total_revenue(self):
        """获取累计收入"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM Charge")
            return cursor.fetchone()[0]

    def create_department_page(self, parent):
        """创建科室管理页面"""
        # 创建科室表格
        columns = ("ID", "科室名称", "科室主任", "联系电话", "描述")
        self.dept_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)

        for col in columns:
            self.dept_tree.heading(col, text=col)
            self.dept_tree.column(col, width=150)

        self.dept_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=self.refresh_department_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=self.add_department).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑", command=self.edit_department).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=self.delete_department).pack(side=tk.LEFT, padx=5)

        # 初始加载数据
        self.refresh_department_data()

    def refresh_department_data(self):
        """刷新科室数据"""
        if self.connection:
            # 清空现有数据
            for item in self.dept_tree.get_children():
                self.dept_tree.delete(item)

            # 查询并显示数据
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT dept_id, dept_name, dept_head, contact_phone, description FROM community_hospital_db_2.Department")
                rows = cursor.fetchall()

                for row in rows:
                    self.dept_tree.insert("", tk.END, values=row)

    def add_department(self):
        """添加科室"""
        # 创建添加窗口
        add_window = tk.Toplevel(self.root)
        add_window.title("添加科室")
        add_window.geometry("400x300")

        # 表单字段
        ttk.Label(add_window, text="科室名称:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        dept_name = ttk.Entry(add_window, width=30)
        dept_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(add_window, text="科室主任:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        dept_head = ttk.Entry(add_window, width=30)
        dept_head.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(add_window, text="联系电话:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        contact_phone = ttk.Entry(add_window, width=30)
        contact_phone.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(add_window, text="描述:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        description = tk.Text(add_window, width=30, height=5)
        description.grid(row=3, column=1, padx=10, pady=5)

        # 按钮
        def save_department():
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO community_hospital_db_2.Department (dept_name, dept_head, contact_phone, description) VALUES (%s, %s, %s, %s)",
                        (dept_name.get(), dept_head.get(), contact_phone.get(), description.get("1.0", tk.END).strip())
                    )
                self.connection.commit()
                # 将插入的逆操作（删除该记录）推入撤销栈
                try:
                    last_id = cursor.lastrowid
                    id_col = self.get_primary_key_column('Department')
                    self.push_undo({'type': 'delete', 'table': 'Department', 'id_column': id_col, 'id': last_id})
                except Exception:
                    pass
                messagebox.showinfo("成功", "科室添加成功")
                add_window.destroy()
                self.refresh_department_data()
                # 更新统计信息
                self.update_statistics(self.stats_frame)
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        # 保存和清空按钮
        btn_frame = ttk.Frame(add_window)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="保存", command=save_department).pack(side=tk.LEFT, padx=5)
        def clear_department_form():
            dept_name.delete(0, tk.END)
            dept_head.delete(0, tk.END)
            contact_phone.delete(0, tk.END)
            description.delete("1.0", tk.END)

        ttk.Button(btn_frame, text="清空", command=clear_department_form).pack(side=tk.LEFT, padx=5)

    def edit_department(self):
        """编辑科室"""
        selected = self.dept_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要编辑的科室")
            return

        item = self.dept_tree.item(selected[0])
        dept_id = item['values'][0]

        # 获取当前数据
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT dept_name, dept_head, contact_phone, description FROM community_hospital_db_2.Department WHERE dept_id = %s",
                           (dept_id,))
            dept_data = cursor.fetchone()

        # 创建编辑窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑科室")
        edit_window.geometry("400x300")

        # 表单字段
        ttk.Label(edit_window, text="科室名称:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        dept_name = ttk.Entry(edit_window, width=30)
        dept_name.grid(row=0, column=1, padx=10, pady=5)
        dept_name.insert(0, dept_data[0])

        ttk.Label(edit_window, text="科室主任:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        dept_head = ttk.Entry(edit_window, width=30)
        dept_head.grid(row=1, column=1, padx=10, pady=5)
        dept_head.insert(0, dept_data[1])

        ttk.Label(edit_window, text="联系电话:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        contact_phone = ttk.Entry(edit_window, width=30)
        contact_phone.grid(row=2, column=1, padx=10, pady=5)
        contact_phone.insert(0, dept_data[2])

        ttk.Label(edit_window, text="描述:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        description = tk.Text(edit_window, width=30, height=5)
        description.grid(row=3, column=1, padx=10, pady=5)
        description.insert("1.0", dept_data[3])

        # 按钮
        def update_department():
            try:
                # 在更新前获取旧数据以支持撤销
                try:
                    old = None
                    with self.connection.cursor() as _c:
                        _c.execute("SELECT * FROM Department WHERE dept_id = %s", (dept_id,))
                        row = _c.fetchone()
                        if row:
                            _c.execute("DESCRIBE Department")
                            cols = [c[0] for c in _c.fetchall()]
                            old = dict(zip(cols, row))
                except Exception:
                    pass
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE community_hospital_db_2.Department SET dept_name=%s, dept_head=%s, contact_phone=%s, description=%s WHERE dept_id=%s",
                        (dept_name.get(), dept_head.get(), contact_phone.get(), description.get("1.0", tk.END).strip(),
                         dept_id)
                    )
                self.connection.commit()
                messagebox.showinfo("成功", "科室更新成功")
                edit_window.destroy()
                self.refresh_department_data()
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {str(e)}")

        ttk.Button(edit_window, text="更新", command=update_department).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_department(self):
        """删除科室"""
        selected = self.dept_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要删除的科室")
            return

        item = self.dept_tree.item(selected[0])
        dept_id = item['values'][0]

        if messagebox.askyesno("确认", "确定要删除这个科室吗？"):
            try:
                # 在删除前备份整行以便撤销（插回）
                old = self.fetch_row_by_id('Department', 'dept_id', dept_id)
                with self.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Department WHERE dept_id = %s", (dept_id,))
                self.connection.commit()
                if old:
                    self.push_undo({'type': 'insert', 'table': 'Department', 'data': old})
                messagebox.showinfo("成功", "科室删除成功")
                self.refresh_department_data()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def create_staff_page(self, parent):
        """创建员工管理页面"""
        # 创建员工表格
        columns = ("ID", "工号", "姓名", "性别", "职位", "科室ID", "职称", "电话", "邮箱", "入职日期", "状态")
        self.staff_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)

        for col in columns:
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=100)

        self.staff_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=self.refresh_staff_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=self.add_staff).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑", command=self.edit_staff).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=self.delete_staff).pack(side=tk.LEFT, padx=5)

        # 初始加载数据
        self.refresh_staff_data()

    def refresh_staff_data(self):
        """刷新员工数据"""
        if self.connection:
            # 清空现有数据
            for item in self.staff_tree.get_children():
                self.staff_tree.delete(item)

            # 查询并显示数据
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT staff_id, staff_number, staff_name, gender, position, dept_id, title, phone, email, hire_date, status FROM community_hospital_db_2.Staff")
                rows = cursor.fetchall()

                for row in rows:
                    self.staff_tree.insert("", tk.END, values=row)

    def add_staff(self):
        """添加员工"""
        # 创建添加窗口
        add_window = tk.Toplevel(self.root)
        add_window.title("添加员工")
        add_window.geometry("500x400")

        # 表单字段
        fields = [
            ("工号:", "staff_number"),
            ("姓名:", "staff_name"),
            ("性别:", "gender"),
            ("职位:", "position"),
            ("科室ID:", "dept_id"),
            ("职称:", "title"),
            ("电话:", "phone"),
            ("邮箱:", "email"),
            ("入职日期:", "hire_date"),
            ("状态:", "status")
        ]

        entries = {}
        for i, (label, field_name) in enumerate(fields):
            ttk.Label(add_window, text=label).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(add_window, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field_name] = entry

        # 按钮
        def save_staff():
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Staff (staff_number, staff_name, gender, position, dept_id, title, phone, email, hire_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (entries["staff_number"].get(), entries["staff_name"].get(), entries["gender"].get(),
                         entries["position"].get(), entries["dept_id"].get(), entries["title"].get(),
                         entries["phone"].get(), entries["email"].get(), entries["hire_date"].get(),
                         entries["status"].get())
                    )
                self.connection.commit()
                # 推入撤销（删除这条新插入的员工）
                try:
                    last_id = cursor.lastrowid
                    id_col = self.get_primary_key_column('Staff')
                    self.push_undo({'type': 'delete', 'table': 'Staff', 'id_column': id_col, 'id': last_id})
                except Exception:
                    pass
                messagebox.showinfo("成功", "员工添加成功")
                add_window.destroy()
                self.refresh_staff_data()
                # 更新统计信息
                self.update_statistics(self.stats_frame)
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        ttk.Button(add_window, text="保存", command=save_staff).grid(row=len(fields), column=0, columnspan=2, pady=10)
        # 添加清空按钮，重置所有输入框
        def clear_staff_form():
            for e in entries.values():
                e.delete(0, tk.END)

        ttk.Button(add_window, text="清空", command=clear_staff_form).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

    def edit_staff(self):
        """编辑员工"""
        selected = self.staff_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要编辑的员工")
            return

        item = self.staff_tree.item(selected[0])
        staff_id = item['values'][0]

        # 获取当前数据
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT staff_number, staff_name, gender, position, dept_id, title, phone, email, hire_date, status FROM Staff WHERE staff_id = %s",
                (staff_id,))
            staff_data = cursor.fetchone()

        # 创建编辑窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑员工")
        edit_window.geometry("500x400")

        # 表单字段
        fields = [
            ("工号:", "staff_number"),
            ("姓名:", "staff_name"),
            ("性别:", "gender"),
            ("职位:", "position"),
            ("科室ID:", "dept_id"),
            ("职称:", "title"),
            ("电话:", "phone"),
            ("邮箱:", "email"),
            ("入职日期:", "hire_date"),
            ("状态:", "status")
        ]

        entries = {}
        for i, (label, field_name) in enumerate(fields):
            ttk.Label(edit_window, text=label).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, staff_data[i])
            entries[field_name] = entry

        # 按钮
        def update_staff():
            try:
                # 备份旧数据以便撤销
                try:
                    old = self.fetch_row_by_id('Staff', 'staff_id', staff_id)
                    if old:
                        self.push_undo({'type': 'update', 'table': 'Staff', 'id_column': 'staff_id', 'id': staff_id, 'data': old})
                except Exception:
                    pass
                with self.connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE Staff SET staff_number=%s, staff_name=%s, gender=%s, position=%s, dept_id=%s, title=%s, phone=%s, email=%s, hire_date=%s, status=%s WHERE staff_id=%s",
                        (entries["staff_number"].get(), entries["staff_name"].get(), entries["gender"].get(),
                         entries["position"].get(), entries["dept_id"].get(), entries["title"].get(),
                         entries["phone"].get(), entries["email"].get(), entries["hire_date"].get(),
                         entries["status"].get(), staff_id)
                    )
                self.connection.commit()
                messagebox.showinfo("成功", "员工更新成功")
                edit_window.destroy()
                self.refresh_staff_data()
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {str(e)}")

        ttk.Button(edit_window, text="更新", command=update_staff).grid(row=len(fields), column=0, columnspan=2,
                                                                        pady=10)

    def delete_staff(self):
        """删除员工"""
        selected = self.staff_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要删除的员工")
            return

        item = self.staff_tree.item(selected[0])
        staff_id = item['values'][0]

        if messagebox.askyesno("确认", "确定要删除这个员工吗？"):
            try:
                old = self.fetch_row_by_id('Staff', 'staff_id', staff_id)
                with self.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Staff WHERE staff_id = %s", (staff_id,))
                self.connection.commit()
                if old:
                    self.push_undo({'type': 'insert', 'table': 'Staff', 'data': old})
                messagebox.showinfo("成功", "员工删除成功")
                self.refresh_staff_data()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def create_patient_page(self, parent):
        """创建患者管理页面"""
        # 创建患者表格
        columns = (
            "ID", "身份证号", "姓名", "性别", "出生日期", "电话", "地址", "紧急联系人", "紧急电话", "有保险", "保险号",
            "注册日期"
        )
        self.patient_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)

        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=120)

        self.patient_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=self.refresh_patient_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=self.add_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑", command=self.edit_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=self.delete_patient).pack(side=tk.LEFT, padx=5)

        # 初始加载数据
        self.refresh_patient_data()

    def refresh_patient_data(self):
        """刷新患者数据"""
        if self.connection:
            # 清空现有数据
            for item in self.patient_tree.get_children():
                self.patient_tree.delete(item)

            # 查询并显示数据
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT patient_id, id_number, full_name, gender, date_of_birth, phone, address, emergency_contact, emergency_phone, has_insurance, insurance_number, registration_date FROM Patient"
                )
                rows = cursor.fetchall()

                for row in rows:
                    self.patient_tree.insert("", tk.END, values=row)

    def add_patient(self):
        """添加患者"""
        add_window = tk.Toplevel(self.root)
        add_window.title("添加患者")
        add_window.geometry("600x400")

        # 表单字段
        fields = [
            ("身份证号:", "id_number"),
            ("姓名:", "full_name"),
            ("性别:", "gender"),
            ("出生日期:", "date_of_birth"),
            ("电话:", "phone"),
            ("地址:", "address"),
            ("紧急联系人:", "emergency_contact"),
            ("紧急电话:", "emergency_phone"),
            ("有保险:", "has_insurance"),
            ("保险号:", "insurance_number"),
            ("注册日期:", "registration_date")  # 新增
        ]

        entries = {}
        for i, (label, field_name) in enumerate(fields):
            ttk.Label(add_window, text=label).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(add_window, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field_name] = entry

        # 按钮
        def save_patient():
            try:
                # 处理字段转换（与原代码保持一致）
                has_insurance = 1 if entries["has_insurance"].get().lower() in ['true', '1', 'yes', '是'] else 0
                insurance_number = entries["insurance_number"].get()
                if insurance_number == "":
                    insurance_number = None

                registration_date = entries["registration_date"].get()

                with self.connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO community_hospital_db_2.Patient (id_number, full_name, gender, date_of_birth, phone, address, emergency_contact, emergency_phone, has_insurance, insurance_number, registration_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            entries["id_number"].get(),
                            entries["full_name"].get(),
                            entries["gender"].get(),
                            entries["date_of_birth"].get(),
                            entries["phone"].get(),
                            entries["address"].get(),
                            entries["emergency_contact"].get(),
                            entries["emergency_phone"].get(),
                            has_insurance,
                            insurance_number,
                            registration_date
                        )
                    )
                self.connection.commit()
                # 推入撤销（删除新插入患者）
                try:
                    last_id = cursor.lastrowid
                    id_col = self.get_primary_key_column('Patient')
                    self.push_undo({'type': 'delete', 'table': 'Patient', 'id_column': id_col, 'id': last_id})
                except Exception:
                    pass
                messagebox.showinfo("成功", "患者添加成功")
                add_window.destroy()
                self.refresh_patient_data()
                self.update_statistics(self.stats_frame)
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        ttk.Button(add_window, text="保存", command=save_patient).grid(row=len(fields), column=0, columnspan=2, pady=10)
        # 添加清空按钮，重置所有输入框
        def clear_patient_form():
            for e in entries.values():
                e.delete(0, tk.END)

        ttk.Button(add_window, text="清空", command=clear_patient_form).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

    def edit_patient(self):
        """编辑患者"""
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要编辑的患者")
            return

        item = self.patient_tree.item(selected[0])
        patient_id = item['values'][0]

        # 获取当前数据
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_number, full_name, gender, date_of_birth, phone, address, emergency_contact, emergency_phone, has_insurance, insurance_number, registration_date FROM Patient WHERE patient_id = %s",
                (patient_id,)
            )
            patient_data = cursor.fetchone()

        # 创建编辑窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑患者")
        edit_window.geometry("600x400")

        # 表单字段
        fields = [
            ("身份证号:", "id_number"),
            ("姓名:", "full_name"),
            ("性别:", "gender"),
            ("出生日期:", "date_of_birth"),
            ("电话:", "phone"),
            ("地址:", "address"),
            ("紧急联系人:", "emergency_contact"),
            ("紧急电话:", "emergency_phone"),
            ("有保险:", "has_insurance"),
            ("保险号:", "insurance_number"),
            ("注册日期:", "registration_date")  # 新增
        ]

        entries = {}
        for i, (label, field_name) in enumerate(fields):
            ttk.Label(edit_window, text=label).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            if i == 8:  # has_insurance 字段
                entry.insert(0, "True" if patient_data[i] else "False")
            else:
                entry.insert(0, patient_data[i] or "")
            entries[field_name] = entry

        # 按钮
        def update_patient():
            try:
                # 备份旧数据以支持撤销
                try:
                    old = self.fetch_row_by_id('Patient', 'patient_id', patient_id)
                    if old:
                        self.push_undo({'type': 'update', 'table': 'Patient', 'id_column': 'patient_id', 'id': patient_id, 'data': old})
                except Exception:
                    pass
                has_insurance = 1 if entries["has_insurance"].get().lower() in ['true', '1', 'yes', '是'] else 0
                insurance_number = entries["insurance_number"].get()
                if insurance_number == "":
                    insurance_number = None

                registration_date = entries["registration_date"].get()  # 新增

                with self.connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE Patient SET id_number=%s, full_name=%s, gender=%s, date_of_birth=%s, phone=%s, address=%s, emergency_contact=%s, emergency_phone=%s, has_insurance=%s, insurance_number=%s, registration_date=%s WHERE patient_id=%s",
                        (
                            entries["id_number"].get(),
                            entries["full_name"].get(),
                            entries["gender"].get(),
                            entries["date_of_birth"].get(),
                            entries["phone"].get(),
                            entries["address"].get(),
                            entries["emergency_contact"].get(),
                            entries["emergency_phone"].get(),
                            has_insurance,
                            insurance_number,
                            registration_date,
                            patient_id
                        )
                    )
                self.connection.commit()
                messagebox.showinfo("成功", "患者更新成功")
                edit_window.destroy()
                self.refresh_patient_data()
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {str(e)}")

        ttk.Button(edit_window, text="更新", command=update_patient).grid(row=len(fields), column=0, columnspan=2,
                                                                          pady=10)

    def delete_patient(self):
        """删除患者"""
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要删除的患者")
            return

        item = self.patient_tree.item(selected[0])
        patient_id = item['values'][0]

        if messagebox.askyesno("确认", "确定要删除这个患者吗？"):
            try:
                old = self.fetch_row_by_id('Patient', 'patient_id', patient_id)
                with self.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Patient WHERE patient_id = %s", (patient_id,))
                self.connection.commit()
                if old:
                    self.push_undo({'type': 'insert', 'table': 'Patient', 'data': old})
                messagebox.showinfo("成功", "患者删除成功")
                self.refresh_patient_data()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def clear_all_data(self):
        """清空当前数据库中所有表的数据（危险操作，需确认）"""
        if not self.connection:
            messagebox.showerror("错误", "未连接到数据库")
            return

        # 第一层确认（快速弹窗）
        if not messagebox.askyesno("确认清空", "此操作将清空数据库中所有表的数据，无法恢复。确定继续？"):
            return

        db_name = self.connection.db.decode() if isinstance(self.connection.db, bytes) else self.connection.db

        # 第二层确认：要求输入数据库名称以避免误操作
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("二次确认 - 清空数据库")
        confirm_window.geometry("420x140")
        confirm_window.transient(self.root)
        confirm_window.grab_set()

        ttk.Label(confirm_window, text="为了避免误操作，请在下方输入数据库名称以确认清空：").pack(padx=12, pady=(12, 6))
        ttk.Label(confirm_window, text=f"数据库: {db_name}", foreground="red").pack(padx=12, pady=(0, 6))

        confirm_entry = ttk.Entry(confirm_window, width=40)
        confirm_entry.pack(padx=12, pady=(0, 8))

        def perform_clear():
            # 确认文本必须与数据库名完全匹配
            if confirm_entry.get() != str(db_name):
                messagebox.showerror("错误", "确认文本与数据库名不匹配，操作已取消")
                return

            try:
                with self.connection.cursor() as cursor:
                    # 获取当前数据库的所有表名
                    cursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = %s", (db_name,))
                    tables = [row[0] for row in cursor.fetchall()]

                    # 先备份所有表的数据以支持撤销（可能较大）
                    backup = {}
                    for table in tables:
                        try:
                            cursor.execute(f"SELECT * FROM `{table}`")
                            rows = cursor.fetchall()
                            cursor.execute(f"DESCRIBE `{table}`")
                            cols = [c[0] for c in cursor.fetchall()]
                            backup[table] = [dict(zip(cols, r)) for r in rows]
                        except Exception as e:
                            print(f"备份表 {table} 时失败: {e}")

                    # 将备份推入撤销栈
                    if backup:
                        self.push_undo({'type': 'bulk_restore', 'data': backup})

                    # 关闭外键检查，逐表清空
                    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                    for table in tables:
                        try:
                            cursor.execute(f"TRUNCATE TABLE `{table}`;")
                        except Exception:
                            # 如果 TRUNCATE 因某些原因失败，尝试 DELETE
                            try:
                                cursor.execute(f"DELETE FROM `{table}`;")
                            except Exception as e:
                                # 记录失败并继续尝试其它表
                                print(f"清空表 {table} 失败: {e}")
                    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
                self.connection.commit()
                messagebox.showinfo("成功", "已清空数据库中所有表的数据")

                # 刷新主界面已知表格和统计信息（存在则刷新）
                try:
                    if hasattr(self, "refresh_department_data"):
                        self.refresh_department_data()
                    if hasattr(self, "refresh_staff_data"):
                        self.refresh_staff_data()
                    if hasattr(self, "refresh_patient_data"):
                        self.refresh_patient_data()
                    if hasattr(self, "stats_frame"):
                        self.update_statistics(self.stats_frame)
                except Exception as e:
                    print(f"刷新界面时发生错误: {e}")
            except Exception as e:
                # 尝试确保外键检查被恢复
                try:
                    with self.connection.cursor() as cursor:
                        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
                    self.connection.commit()
                except Exception:
                    pass
                messagebox.showerror("错误", f"清空数据失败: {e}")
            finally:
                confirm_window.grab_release()
                confirm_window.destroy()

        def cancel_confirm():
            confirm_window.grab_release()
            confirm_window.destroy()

        btn_frame = ttk.Frame(confirm_window)
        btn_frame.pack(pady=(0, 8))
        ttk.Button(btn_frame, text="确认清空", command=perform_clear).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame, text="取消", command=cancel_confirm).pack(side=tk.LEFT, padx=8)

    def open_department_window(self):
        """打开科室管理窗口"""
        dept_window = tk.Toplevel(self.root)
        dept_window.title("科室管理")
        dept_window.geometry("800x600")

        # 动态从数据库获取列并创建Treeview
        columns_list = self.get_select_columns_list('Department')
        columns = tuple(columns_list)
        dept_tree = ttk.Treeview(dept_window, columns=columns, show="headings", height=20)

        for col in columns:
            dept_tree.heading(col, text=col)
            dept_tree.column(col, width=150)

        dept_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(dept_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=lambda: self.refresh_tree_data(dept_tree, "Department")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=lambda: self.open_add_window("Department", dept_tree)).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑",
                   command=lambda: self.open_edit_window("Department", dept_tree, "dept_id")).pack(side=tk.LEFT,
                                                                                                     padx=5)
        ttk.Button(btn_frame, text="删除",
                   command=lambda: self.open_delete_window("Department", dept_tree, "dept_id")).pack(side=tk.LEFT,
                                                                                                     padx=5)

        # 加载数据
        self.refresh_tree_data(dept_tree, "Department")

    def open_staff_window(self):
        """打开员工管理窗口"""
        staff_window = tk.Toplevel(self.root)
        staff_window.title("员工管理")
        staff_window.geometry("1000x600")

        # 动态从数据库获取列并创建Treeview
        columns_list = self.get_select_columns_list('Staff')
        columns = tuple(columns_list)
        staff_tree = ttk.Treeview(staff_window, columns=columns, show="headings", height=20)

        for col in columns:
            staff_tree.heading(col, text=col)
            staff_tree.column(col, width=100)

        staff_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(staff_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=lambda: self.refresh_tree_data(staff_tree, "Staff")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=lambda: self.open_add_window("Staff", staff_tree)).pack(side=tk.LEFT,
                                                                                                           padx=5)
        ttk.Button(btn_frame, text="编辑", command=lambda: self.open_edit_window("Staff", staff_tree, "staff_id")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除",
                   command=lambda: self.open_delete_window("Staff", staff_tree, "staff_id")).pack(side=tk.LEFT, padx=5)

        # 加载数据
        self.refresh_tree_data(staff_tree, "Staff")

    def open_doctor_window(self):
        """打开医生管理窗口"""
        doctor_window = tk.Toplevel(self.root)
        doctor_window.title("医生管理")
        doctor_window.geometry("800x600")

        columns_list = self.get_select_columns_list('Doctor')
        columns = tuple(columns_list)
        doctor_tree = ttk.Treeview(doctor_window, columns=columns, show="headings", height=20)

        for col in columns:
            doctor_tree.heading(col, text=col)
            doctor_tree.column(col, width=150)

        doctor_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(doctor_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=lambda: self.refresh_tree_data(doctor_tree, "Doctor")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=lambda: self.open_add_window("Doctor", doctor_tree)).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑",
                   command=lambda: self.open_edit_window("Doctor", doctor_tree, "doctor_id")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除",
                   command=lambda: self.open_delete_window("Doctor", doctor_tree, "doctor_id")).pack(side=tk.LEFT,
                                                                                                     padx=5)

        # 加载数据
        self.refresh_tree_data(doctor_tree, "Doctor")

    def open_room_window(self):
        """打开诊室管理窗口"""
        room_window = tk.Toplevel(self.root)
        room_window.title("诊室管理")
        room_window.geometry("800x600")

        columns_list = self.get_select_columns_list('ConsultationRoom')
        columns = tuple(columns_list)
        room_tree = ttk.Treeview(room_window, columns=columns, show="headings", height=20)

        for col in columns:
            room_tree.heading(col, text=col)
            room_tree.column(col, width=120)

        room_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(room_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=lambda: self.refresh_tree_data(room_tree, "ConsultationRoom")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=lambda: self.open_add_window("ConsultationRoom", room_tree)).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑",
                   command=lambda: self.open_edit_window("ConsultationRoom", room_tree, "room_id")).pack(side=tk.LEFT,
                                                                                                         padx=5)
        ttk.Button(btn_frame, text="删除",
                   command=lambda: self.open_delete_window("ConsultationRoom", room_tree, "room_id")).pack(side=tk.LEFT,
                                                                                                           padx=5)

        # 加载数据
        self.refresh_tree_data(room_tree, "ConsultationRoom")

    def open_patient_window(self):
        """打开患者管理窗口"""
        patient_window = tk.Toplevel(self.root)
        patient_window.title("患者管理")
        patient_window.geometry("1000x600")

        columns_list = self.get_select_columns_list('Patient')
        columns = tuple(columns_list)
        patient_tree = ttk.Treeview(patient_window, columns=columns, show="headings", height=20)

        for col in columns:
            patient_tree.heading(col, text=col)
            patient_tree.column(col, width=120)

        patient_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(patient_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=lambda: self.refresh_tree_data(patient_tree, "Patient")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=lambda: self.open_add_window("Patient", patient_tree)).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑",
                   command=lambda: self.open_edit_window("Patient", patient_tree, "patient_id")).pack(side=tk.LEFT,
                                                                                                      padx=5)
        ttk.Button(btn_frame, text="删除",
                   command=lambda: self.open_delete_window("Patient", patient_tree, "patient_id")).pack(side=tk.LEFT,
                                                                                                        padx=5)

        # 加载数据
        self.refresh_tree_data(patient_tree, "Patient")

    def open_appointment_window(self):
        """打开预约管理窗口"""
        appointment_window = tk.Toplevel(self.root)
        appointment_window.title("预约管理")
        appointment_window.geometry("1000x600")

        columns_list = self.get_select_columns_list('Appointment')
        columns = tuple(columns_list)
        appointment_tree = ttk.Treeview(appointment_window, columns=columns, show="headings", height=20)

        for col in columns:
            appointment_tree.heading(col, text=col)
            appointment_tree.column(col, width=120)

        appointment_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(appointment_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新", command=lambda: self.refresh_tree_data(appointment_tree, "Appointment")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加", command=lambda: self.open_add_window("Appointment", appointment_tree)).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑",
                   command=lambda: self.open_edit_window("Appointment", appointment_tree, "appointment_id")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除",
                   command=lambda: self.open_delete_window("Appointment", appointment_tree, "appointment_id")).pack(
            side=tk.LEFT, padx=5)

        # 加载数据
        self.refresh_tree_data(appointment_tree, "Appointment")



    def refresh_tree_data(self, tree, table_name, select_columns=None):
        """刷新树形控件数据"""
        if self.connection:
            # 清空现有数据
            for item in tree.get_children():
                tree.delete(item)

            # 获取列信息并构建select_columns（如果未传入）
            if not select_columns:
                col_list = self.get_select_columns_list(table_name)
                select_columns_str = ', '.join(col_list)
            else:
                # 允许传入逗号分隔字符串或列表
                if isinstance(select_columns, (list, tuple)):
                    col_list = list(select_columns)
                    select_columns_str = ', '.join(col_list)
                else:
                    # 清理并分割字符串
                    col_list = [c.strip() for c in select_columns.split(',') if c.strip()]
                    select_columns_str = ', '.join(col_list)

            # 查询并显示数据
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT {select_columns_str} FROM {table_name}")
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", tk.END, values=row)

    def get_select_columns_list(self, table_name):
        """返回表的列名列表（按表定义顺序）"""
        with self.connection.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table_name}")
            columns_info = cursor.fetchall()
            return [col[0] for col in columns_info]

    def get_select_columns(self, table_name):
        """获取表的列名（逗号分隔字符串）"""
        return ', '.join(self.get_select_columns_list(table_name))

    def open_add_window(self, table_name, tree):
        """打开添加窗口"""
        # 获取表的列信息
        with self.connection.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table_name}")
            columns_info = cursor.fetchall()

        # 创建添加窗口
        add_window = tk.Toplevel(self.root)
        add_window.title(f"添加{table_name}")
        add_window.geometry("500x400")

        # 创建表单
        entries = {}
        row_idx = 0
        for col_info in columns_info:
            col_name = col_info[0]
            extra = col_info[5] or ''
            # 跳过自增主键，仅基于extra判断，不再无差别跳过特定列名
            if 'auto_increment' in extra:
                continue

            ttk.Label(add_window, text=f"{col_name}:").grid(row=row_idx, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(add_window, width=30)
            entry.grid(row=row_idx, column=1, padx=10, pady=5)
            entries[col_name] = entry
            row_idx += 1

        # 按钮
        def save_data():
            try:
                with self.connection.cursor() as cursor:
                    # 构建INSERT语句
                    col_names = list(entries.keys())
                    placeholders = ['%s'] * len(col_names)
                    sql = f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({', '.join(placeholders)})"
                    values = [entries[col].get() for col in col_names]
                    cursor.execute(sql, values)
                self.connection.commit()
                # 将插入操作可撤销（删除插入的记录）
                try:
                    last_id = cursor.lastrowid
                    id_col = self.get_primary_key_column(table_name)
                    self.push_undo({'type': 'delete', 'table': table_name, 'id_column': id_col, 'id': last_id})
                except Exception:
                    pass
                messagebox.showinfo("成功", f"{table_name}添加成功")
                add_window.destroy()
                self.refresh_tree_data(tree, table_name, self.get_select_columns(table_name))
                # 更新统计信息
                self.update_statistics(self.stats_frame)
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        # 保存和清空按钮
        btn_frame = ttk.Frame(add_window)
        btn_frame.grid(row=row_idx + 1, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="保存", command=save_data).pack(side=tk.LEFT, padx=5)

        def clear_generic_form():
            for ent in entries.values():
                ent.delete(0, tk.END)

        ttk.Button(btn_frame, text="清空", command=clear_generic_form).pack(side=tk.LEFT, padx=5)

    def open_edit_window(self, table_name, tree, id_column):
        """打开编辑窗口"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("警告", f"请选择要编辑的{table_name}")
            return

        item = tree.item(selected[0])
        record_id = item['values'][0]

        # 获取表的列信息
        with self.connection.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table_name}")
            columns_info = cursor.fetchall()
            col_names = [col[0] for col in columns_info]

        # 获取当前记录数据
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} WHERE {id_column} = %s", (record_id,))
            current_data = cursor.fetchone()

        # 创建编辑窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"编辑{table_name}")
        edit_window.geometry("500x400")

        # 创建表单
        entries = {}
        row_idx = 0
        for col_info in columns_info:
            col_name = col_info[0]
            # 跳过主键
            if col_name == id_column:
                continue

            ttk.Label(edit_window, text=f"{col_name}:").grid(row=row_idx, column=0, sticky=tk.W, padx=10, pady=5)
            entry = ttk.Entry(edit_window, width=30)
            entry.grid(row=row_idx, column=1, padx=10, pady=5)
            # 使用列名在current_data中的索引来取值，保证字段与数据库列正确对应
            try:
                idx = col_names.index(col_name)
                val = current_data[idx]
            except Exception:
                val = None
            entry.insert(0, str(val) if val is not None else "")
            entries[col_name] = entry
            row_idx += 1

        # 按钮
        def update_data():
            try:
                # 备份旧数据以便撤销
                try:
                    old = None
                    with self.connection.cursor() as _c:
                        _c.execute(f"SELECT * FROM {table_name} WHERE {id_column} = %s", (record_id,))
                        row = _c.fetchone()
                        if row:
                            _c.execute(f"DESCRIBE {table_name}")
                            cols = [c[0] for c in _c.fetchall()]
                            old = dict(zip(cols, row))
                except Exception:
                    pass
                with self.connection.cursor() as cursor:
                    # 构建UPDATE语句
                    set_clause = ', '.join([f"`{col}` = %s" for col in entries.keys()])
                    sql = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
                    values = [entries[col].get() for col in entries.keys()] + [record_id]
                    cursor.execute(sql, values)
                self.connection.commit()
                messagebox.showinfo("成功", f"{table_name}更新成功")
                edit_window.destroy()
                self.refresh_tree_data(tree, table_name, self.get_select_columns(table_name))
            except Exception as e:
                messagebox.showerror("错误", f"更新失败: {str(e)}")

        ttk.Button(edit_window, text="更新", command=update_data).grid(row=row_idx + 1, column=0, columnspan=2,
                                                                       pady=10)

    def open_delete_window(self, table_name, tree, id_column):
        """打开删除窗口"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("警告", f"请选择要删除的{table_name}")
            return

        item = tree.item(selected[0])
        record_id = item['values'][0]

        if messagebox.askyesno("确认", f"确定要删除这个{table_name}吗？"):
            try:
                # 备份整行
                old = self.fetch_row_by_id(table_name, id_column, record_id)
                with self.connection.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (record_id,))
                self.connection.commit()
                if old:
                    self.push_undo({'type': 'insert', 'table': table_name, 'data': old})
                messagebox.showinfo("成功", f"{table_name}删除成功")
                self.refresh_tree_data(tree, table_name, self.get_select_columns(table_name))
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def open_revenue_analysis(self):
        """打开收入统计窗口"""
        revenue_window = tk.Toplevel(self.root)
        revenue_window.title("收入统计")
        revenue_window.geometry("800x600")

        # 创建收入统计界面
        columns = ("日期", "收入总额", "就诊次数", "平均消费")
        revenue_tree = ttk.Treeview(revenue_window, columns=columns, show="headings", height=20)

        for col in columns:
            revenue_tree.heading(col, text=col)
            revenue_tree.column(col, width=180)

        revenue_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 按钮框架
        btn_frame = ttk.Frame(revenue_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(btn_frame, text="刷新数据", command=lambda: self.refresh_revenue_data(revenue_tree)).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="查看详细", command=lambda: self.view_detailed_revenue()).pack(side=tk.LEFT, padx=5)

        # 加载数据
        self.refresh_revenue_data(revenue_tree)

    def refresh_revenue_data(self, tree):
        """刷新收入统计数据"""
        if self.connection:
            # 清空现有数据
            for item in tree.get_children():
                tree.delete(item)

            # 查询收入统计
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        DATE(v.checkin_time) as date,
                        SUM(c.total_amount) as total_revenue,
                        COUNT(v.visit_id) as visit_count,
                        AVG(c.total_amount) as avg_cost
                    FROM Visit v
                    JOIN Charge c ON v.visit_id = c.visit_id
                    GROUP BY DATE(v.checkin_time)
                    ORDER BY date DESC
                    LIMIT 30
                """)
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", tk.END, values=row)

    def view_detailed_revenue(self):
        """查看详细收入信息"""
        detailed_window = tk.Toplevel(self.root)
        detailed_window.title("详细收入信息")
        detailed_window.geometry("1000x600")

        # 创建详细收入表格
        columns = ("就诊ID", "患者姓名", "医生姓名", "就诊日期", "诊断", "费用")
        detailed_tree = ttk.Treeview(detailed_window, columns=columns, show="headings", height=20)

        for col in columns:
            detailed_tree.heading(col, text=col)
            detailed_tree.column(col, width=150)

        detailed_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 刷新按钮
        ttk.Button(detailed_window, text="刷新",
                   command=lambda: self.refresh_detailed_revenue_data(detailed_tree)).pack(pady=5)

        # 加载数据
        self.refresh_detailed_revenue_data(detailed_tree)

    def refresh_detailed_revenue_data(self, tree):
        """刷新详细收入数据"""
        if self.connection:
            # 清空现有数据
            for item in tree.get_children():
                tree.delete(item)

            # 查询详细收入信息
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        v.visit_id,
                        p.full_name as patient_name,
                        s.staff_name as doctor_name,
                        v.checkin_time,
                        v.diagnosis,
                        c.consultation_fee as cost
                    FROM Visit v
                    JOIN Patient p ON v.patient_id = p.patient_id
                    JOIN Staff s ON v.doctor_id = s.staff_id
                    JOIN Charge c ON v.visit_id = c.visit_id
                    ORDER BY v.checkin_time DESC
                    LIMIT 100
                """)
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", tk.END, values=row)

    def open_appointment_analysis(self):
        """打开预约统计窗口"""
        appointment_window = tk.Toplevel(self.root)
        appointment_window.title("预约统计")
        appointment_window.geometry("800x600")

        # 创建预约统计界面
        columns = ("日期", "预约总数", "已确认", "已取消", "就诊率")
        appointment_tree = ttk.Treeview(appointment_window, columns=columns, show="headings", height=20)

        for col in columns:
            appointment_tree.heading(col, text=col)
            appointment_tree.column(col, width=150)

        appointment_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 刷新按钮
        ttk.Button(appointment_window, text="刷新",
                   command=lambda: self.refresh_appointment_data(appointment_tree)).pack(pady=5)

        # 加载数据
        self.refresh_appointment_data(appointment_tree)

    def refresh_appointment_data(self, tree):
        """刷新预约统计数据"""
        if self.connection:
            # 清空现有数据
            for item in tree.get_children():
                tree.delete(item)

            # 查询预约统计
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        appointment_date,
                        COUNT(*) as total_appointments,
                        SUM(CASE WHEN status = 'Confirmed' THEN 1 ELSE 0 END) as confirmed,
                        SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
                        (SUM(CASE WHEN status = 'Confirmed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as attendance_rate
                    FROM Appointment
                    GROUP BY appointment_date
                    ORDER BY appointment_date DESC
                    LIMIT 30
                """)
                rows = cursor.fetchall()

                for row in rows:
                    tree.insert("", tk.END, values=row)


def main():
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()


def get_connection():
    return None
