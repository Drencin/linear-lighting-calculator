from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
import math

class ParameterCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 10, 20, 10]
        self.spacing = 10
        
        self.create_ui()
    
    def create_ui(self):
        # === 标题区域 ===
        title_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1))
        title = Label(
            text='线性照明参数计算器',
            size_hint=(1, 0.7),
            font_size='24sp',
            bold=True,
            color=(0.1, 0.3, 0.6, 1)
        )
        subtitle = Label(
            text='椭圆截面管道流体力学计算',
            size_hint=(1, 0.3),
            font_size='14sp',
            color=(0.4, 0.4, 0.4, 1)
        )
        title_layout.add_widget(title)
        title_layout.add_widget(subtitle)
        self.add_widget(title_layout)

        # === 说明文字区域 ===
        instruction_text = (
            "使用说明：\n"
            "• 在任意三个参数中输入已知值\n"
            "• 留空一个参数作为计算目标\n"
            "• 系统自动计算缺失参数和角度α"
        )
        instruction_label = Label(
            text=instruction_text,
            size_hint=(1, 0.15),
            text_size=(Window.width - 40, None),
            halign='left',
            valign='middle',
            font_size='13sp',
            color=(0.2, 0.2, 0.2, 1)
        )
        instruction_label.bind(size=instruction_label.setter('text_size'))
        self.add_widget(instruction_label)

        # === 输入参数区域 ===
        input_layout = BoxLayout(orientation='vertical', spacing=8, size_hint=(1, 0.3))
        
        # 参数P
        p_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
        p_layout.add_widget(Label(text='压力 P =', size_hint=(0.4, 1), font_size='16sp'))
        self.p_input = TextInput(
            hint_text='输入压力值',
            multiline=False,
            input_filter='float',
            size_hint=(0.4, 1),
            font_size='16sp',
            background_color=(1, 1, 1, 1)
        )
        p_layout.add_widget(self.p_input)
        p_layout.add_widget(Label(text='MPa', size_hint=(0.2, 1), font_size='16sp'))
        input_layout.add_widget(p_layout)

        # 参数e
        e_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
        e_layout.add_widget(Label(text='弹性模量 e =', size_hint=(0.4, 1), font_size='16sp'))
        self.e_input = TextInput(
            hint_text='输入弹性模量',
            multiline=False,
            input_filter='float',
            size_hint=(0.4, 1),
            font_size='16sp',
            background_color=(1, 1, 1, 1)
        )
        e_layout.add_widget(self.e_input)
        e_layout.add_widget(Label(text='GPa', size_hint=(0.2, 1), font_size='16sp'))
        input_layout.add_widget(e_layout)

        # 参数D
        d_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
        d_layout.add_widget(Label(text='直径 D =', size_hint=(0.4, 1), font_size='16sp'))
        self.d_input = TextInput(
            hint_text='输入管道直径',
            multiline=False,
            input_filter='float',
            size_hint=(0.4, 1),
            font_size='16sp',
            background_color=(1, 1, 1, 1)
        )
        d_layout.add_widget(self.d_input)
        d_layout.add_widget(Label(text='mm', size_hint=(0.2, 1), font_size='16sp'))
        input_layout.add_widget(d_layout)

        # 参数L
        l_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
        l_layout.add_widget(Label(text='长度 L =', size_hint=(0.4, 1), font_size='16sp'))
        self.l_input = TextInput(
            hint_text='输入椭圆长轴',
            multiline=False,
            input_filter='float',
            size_hint=(0.4, 1),
            font_size='16sp',
            background_color=(1, 1, 1, 1)
        )
        l_layout.add_widget(self.l_input)
        l_layout.add_widget(Label(text='mm', size_hint=(0.2, 1), font_size='16sp'))
        input_layout.add_widget(l_layout)

        self.add_widget(input_layout)

        # === 按钮区域 ===
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.08))
        
        calc_btn = Button(
            text='开始计算',
            background_color=(0.2, 0.6, 1, 1),
            size_hint=(0.6, 1),
            font_size='18sp'
        )
        calc_btn.bind(on_press=self.calculate)
        
        clear_btn = Button(
            text='清空重置',
            background_color=(0.9, 0.3, 0.3, 1),
            size_hint=(0.4, 1),
            font_size='18sp'
        )
        clear_btn.bind(on_press=self.clear_inputs)
        
        button_layout.add_widget(calc_btn)
        button_layout.add_widget(clear_btn)
        self.add_widget(button_layout)

        # === 结果显示区域 ===
        result_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.12))
        
        alpha_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))
        alpha_layout.add_widget(Label(text='椭圆角度 α =', size_hint=(0.6, 1), font_size='18sp'))
        self.alpha_result = Label(
            text='0.00',
            size_hint=(0.3, 1),
            font_size='18sp',
            color=(0, 0.5, 0, 1)
        )
        alpha_layout.add_widget(self.alpha_result)
        alpha_layout.add_widget(Label(text='°', size_hint=(0.1, 1), font_size='18sp'))
        result_layout.add_widget(alpha_layout)

        self.status_label = Label(
            text='请输入参数开始计算',
            size_hint=(1, 0.5),
            font_size='14sp',
            color=(0.3, 0.3, 0.3, 1)
        )
        result_layout.add_widget(self.status_label)

        self.add_widget(result_layout)

        # === 底部图片区域（占50%高度）===
        image_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.5),
            spacing=5
        )
        
        # 包含二维码的说明图片
        try:
            self.info_image = Image(
                source='instructions_with_qr.png',  # 您的图片文件名
                size_hint=(1, 0.85),
                keep_ratio=True,
                allow_stretch=True,
                pos_hint={'center_x': 0.5}
            )
        except:
            # 如果图片不存在，显示占位符
            self.info_image = Label(
                text='[请将 instructions_with_qr.png 图片文件放入应用目录]',
                size_hint=(1, 0.85),
                font_size='14sp',
                color=(0.5, 0.5, 0.5, 1)
            )
        
        # 图片说明文字
        image_label = Label(
            text='扫描二维码获取技术文档与更新信息',
            size_hint=(1, 0.15),
            font_size='12sp',
            color=(0.4, 0.4, 0.4, 1)
        )
        
        image_layout.add_widget(self.info_image)
        image_layout.add_widget(image_label)
        self.add_widget(image_layout)

        # 绑定输入变化事件
        for input_field in [self.p_input, self.e_input, self.d_input, self.l_input]:
            input_field.bind(text=self.on_input_change)

    def on_input_change(self, instance, value):
        """实时监控输入变化"""
        filled_count = sum([
            bool(self.p_input.text.strip()),
            bool(self.e_input.text.strip()), 
            bool(self.d_input.text.strip()),
            bool(self.l_input.text.strip())
        ])
        
        if filled_count == 3:
            self.status_label.text = '参数已就绪，点击计算或自动计算中...'
            self.status_label.color = (0, 0.5, 0, 1)
            # 自动计算
            self.calculate(None)
        elif filled_count == 4:
            self.status_label.text = '请输入3个参数，留空1个要计算的参数'
            self.status_label.color = (1, 0, 0, 1)
        else:
            self.status_label.text = '请输入参数开始计算'
            self.status_label.color = (0.3, 0.3, 0.3, 1)

    def calculate(self, instance):
        try:
            # 获取输入值
            inputs = []
            if self.p_input.text.strip(): 
                inputs.append(('p', float(self.p_input.text)))
            if self.e_input.text.strip(): 
                inputs.append(('e', float(self.e_input.text)))
            if self.d_input.text.strip(): 
                inputs.append(('d', float(self.d_input.text)))
            if self.l_input.text.strip(): 
                inputs.append(('l', float(self.l_input.text)))
            
            # 检查输入数量
            if len(inputs) != 3:
                self.show_popup('输入错误', '请准确输入3个参数，留空1个要计算的参数！')
                return
            
            # 提取参数值
            params = {key: value for key, value in inputs}
            
            # 计算角度（始终计算）
            if 'd' in params and 'l' in params and params['d'] != 0:
                alpha_rad = math.atan(params['l'] / (2 * params['d']))
                alpha_deg = math.degrees(alpha_rad)
                self.alpha_result.text = f'{alpha_deg:.2f}'
            else:
                self.alpha_result.text = 'N/A'
            
            # 确定缺失的参数并计算
            if 'p' not in params:
                result = self.calculate_p(params)
                self.p_input.text = f'{result:.6f}'
                self.p_input.background_color = (0.8, 0.9, 1, 1)
            else:
                self.p_input.background_color = (1, 1, 1, 1)
                
            if 'e' not in params:
                result = self.calculate_e(params)
                self.e_input.text = f'{result:.6f}'
                self.e_input.background_color = (0.8, 0.9, 1, 1)
            else:
                self.e_input.background_color = (1, 1, 1, 1)
                
            if 'd' not in params:
                result = self.calculate_d(params)
                self.d_input.text = f'{result:.6f}'
                self.d_input.background_color = (0.8, 0.9, 1, 1)
            else:
                self.d_input.background_color = (1, 1, 1, 1)
                
            if 'l' not in params:
                result = self.calculate_l(params)
                self.l_input.text = f'{result:.6f}'
                self.l_input.background_color = (0.8, 0.9, 1, 1)
            else:
                self.l_input.background_color = (1, 1, 1, 1)
            
            self.status_label.text = '计算完成！蓝色背景为计算结果'
            self.status_label.color = (0, 0.5, 0, 1)
            
        except ValueError:
            self.show_popup('输入错误', '请输入有效的数字！')
        except ZeroDivisionError:
            self.show_popup('计算错误', '参数值不能为零！')
        except Exception as e:
            self.show_popup('计算错误', f'计算过程中出现错误: {str(e)}')

    def calculate_p(self, params):
        """计算压力 P"""
        alpha_rad = math.atan(params['l'] / (2 * params['d']))
        numerator = params['e'] * 2 * (math.pi ** 2) * params['d'] * params['l']
        denominator = 2 * alpha_rad + math.sin(2 * alpha_rad)
        return numerator / denominator

    def calculate_e(self, params):
        """计算弹性模量 e"""
        alpha_rad = math.atan(params['l'] / (2 * params['d']))
        numerator = params['p'] * (2 * alpha_rad + math.sin(2 * alpha_rad))
        denominator = 2 * (math.pi ** 2) * params['d'] * params['l']
        return numerator / denominator

    def calculate_d(self, params):
        """计算直径 D - 使用迭代法"""
        target = params['p']
        guess = 1.0
        tolerance = 0.0001
        
        for _ in range(50):
            alpha_rad = math.atan(params['l'] / (2 * guess))
            current = (params['e'] * 2 * (math.pi ** 2) * guess * params['l']) / (2 * alpha_rad + math.sin(2 * alpha_rad))
            
            if abs(current - target) < tolerance:
                return guess
                
            # 简单调整
            if current < target:
                guess *= 1.1
            else:
                guess *= 0.9
                
        return guess

    def calculate_l(self, params):
        """计算长度 L - 使用迭代法"""
        target = params['p']
        guess = 1.0
        tolerance = 0.0001
        
        for _ in range(50):
            alpha_rad = math.atan(guess / (2 * params['d']))
            current = (params['e'] * 2 * (math.pi ** 2) * params['d'] * guess) / (2 * alpha_rad + math.sin(2 * alpha_rad))
            
            if abs(current - target) < tolerance:
                return guess
                
            # 简单调整
            if current < target:
                guess *= 1.1
            else:
                guess *= 0.9
                
        return guess

    def clear_inputs(self, instance):
        """清空所有输入"""
        self.p_input.text = ''
        self.e_input.text = ''
        self.d_input.text = ''
        self.l_input.text = ''
        self.alpha_result.text = '0.00'
        self.status_label.text = '请输入参数开始计算'
        self.status_label.color = (0.3, 0.3, 0.3, 1)
        
        # 重置背景色
        for input_field in [self.p_input, self.e_input, self.d_input, self.l_input]:
            input_field.background_color = (1, 1, 1, 1)

    def show_popup(self, title, message):
        """显示弹窗"""
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        popup_label = Label(
            text=message, 
            text_size=(300, None),
            halign='center'
        )
        close_btn = Button(
            text='关闭', 
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 1, 1)
        )
        
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.5)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

class CalculatorApp(App):
    def build(self):
        self.title = '线性照明参数计算器'
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        return ParameterCalculator()

if __name__ == '__main__':
    CalculatorApp().run()
