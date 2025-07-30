# 猜数字游戏 - 智能版
# 随机生成一个1到100的数字
import random
import time
from datetime import datetime
import os

class SmartGuessGame:
    def __init__(self):
        self.game_history = []
        self.stats = {
            'total_games': 0,
            'wins': 0,
            'best_score': float('inf'),
            'average_attempts': 0
        }
        self.achievements = {
            'first_win': False,
            'perfect_guess': False,
            'master_player': False,
            'persistent_player': False
        }
    
    def clear_screen(self):
        """清屏功能"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_smart_hint(self, guess, number, attempt):
        """智能提示系统"""
        if attempt == 1:
            return "开始你的第一次猜测吧！"
        elif attempt == 2:
            if abs(guess - number) <= 10:
                return "很接近了！"
            elif abs(guess - number) <= 25:
                return "方向对了，继续加油！"
            else:
                return "差距有点大，试试其他方向"
        elif attempt == 3:
            if abs(guess - number) <= 5:
                return "非常接近了！就差一点点！"
            elif abs(guess - number) <= 15:
                return "越来越近了！"
            else:
                return "再仔细想想..."
        else:
            if abs(guess - number) <= 3:
                return "就差那么一点点！"
            elif abs(guess - number) <= 8:
                return "很接近了，再试试！"
            else:
                return "继续努力！"
    
    def calculate_difficulty(self):
        """根据历史表现计算难度"""
        if self.stats['total_games'] == 0:
            return "normal"
        
        avg_attempts = self.stats['average_attempts']
        if avg_attempts <= 4:
            return "hard"
        elif avg_attempts <= 6:
            return "normal"
        else:
            return "easy"
    
    def update_stats(self, attempts, won):
        """更新统计数据"""
        self.stats['total_games'] += 1
        if won:
            self.stats['wins'] += 1
            if attempts < self.stats['best_score']:
                self.stats['best_score'] = attempts
        
        # 修复平均尝试次数计算
        if self.stats['total_games'] > 0:
            total_attempts = sum([game['attempts'] for game in self.game_history])
            self.stats['average_attempts'] = total_attempts / self.stats['total_games']
    
    def check_achievements(self, attempts, won):
        """检查成就"""
        achievements_unlocked = []
        
        if won and not self.achievements['first_win']:
            self.achievements['first_win'] = True
            achievements_unlocked.append("🏆 成就解锁：初次胜利！")
        
        if won and attempts == 1 and not self.achievements['perfect_guess']:
            self.achievements['perfect_guess'] = True
            achievements_unlocked.append("🎯 成就解锁：完美猜测！")
        
        if self.stats['wins'] >= 5 and not self.achievements['master_player']:
            self.achievements['master_player'] = True
            achievements_unlocked.append("👑 成就解锁：猜数字大师！")
        
        if self.stats['total_games'] >= 10 and not self.achievements['persistent_player']:
            self.achievements['persistent_player'] = True
            achievements_unlocked.append("💪 成就解锁：坚持不懈！")
        
        for achievement in achievements_unlocked:
            print(achievement)
    
    def show_stats(self):
        """显示统计信息"""
        print("\n📊 游戏统计：")
        print(f"总游戏次数：{self.stats['total_games']}")
        print(f"胜利次数：{self.stats['wins']}")
        if self.stats['total_games'] > 0:
            win_rate = (self.stats['wins'] / self.stats['total_games']) * 100
            print(f"胜率：{win_rate:.1f}%")
        if self.stats['best_score'] != float('inf'):
            print(f"最佳记录：{self.stats['best_score']}次")
        if self.stats['average_attempts'] > 0:
            print(f"平均尝试次数：{self.stats['average_attempts']:.1f}")
        
        # 显示最近表现
        if len(self.game_history) >= 3:
            recent_wins = sum(1 for game in self.game_history[-3:] if game['won'])
            print(f"最近3局胜率：{recent_wins/3*100:.1f}%")
    
    def show_achievements(self):
        """显示成就"""
        print("\n🏆 成就系统：")
        achievements_list = [
            ("初次胜利", self.achievements['first_win']),
            ("完美猜测", self.achievements['perfect_guess']),
            ("猜数字大师", self.achievements['master_player']),
            ("坚持不懈", self.achievements['persistent_player'])
        ]
        
        unlocked_count = 0
        for name, unlocked in achievements_list:
            status = "✅" if unlocked else "❌"
            print(f"{status} {name}")
            if unlocked:
                unlocked_count += 1
        
        print(f"\n成就进度：{unlocked_count}/{len(achievements_list)}")
    
    def show_history(self):
        """显示历史记录"""
        print("\n📜 历史记录：")
        if not self.game_history:
            print("暂无游戏记录")
            return
        
        # 显示最近10局
        recent_games = self.game_history[-10:]
        for i, record in enumerate(recent_games, 1):
            status = "✅" if record['won'] else "❌"
            time_str = f"{record['time']:.1f}秒"
            print(f"{i:2d}. {record['date']} - {status} {record['attempts']}次 ({time_str})")
        
        # 显示统计信息
        if len(self.game_history) > 0:
            total_time = sum(game['time'] for game in self.game_history)
            avg_time = total_time / len(self.game_history)
            print(f"\n📈 历史统计：")
            print(f"总游戏时间：{total_time:.1f}秒")
            print(f"平均游戏时间：{avg_time:.1f}秒")
    
    def play_game(self):
        """主游戏循环"""
        print("🎮 智能猜数字游戏")
        print("=" * 40)
        
        # 选择难度
        difficulty = self.calculate_difficulty()
        if difficulty == "hard":
            max_attempts = 8
            print("🔥 困难模式：最多8次机会")
        elif difficulty == "easy":
            max_attempts = 12
            print("😊 简单模式：最多12次机会")
        else:
            max_attempts = 10
            print("⚖️ 普通模式：最多10次机会")
        
        # 生成数字
        number = random.randint(1, 100)
        guess_count = 0
        start_time = time.time()
        game_won = False
        
        print(f"我已经想好了一个数字（1-100之间），你有{max_attempts}次机会")
        print("💡 提示：我会根据你的猜测给出智能提示！")
        print("💡 提示：输入 'q' 可以退出游戏")
        
        while guess_count < max_attempts:
            guess_count += 1
            remaining = max_attempts - guess_count + 1
            
            try:
                user_input = input(f"\n第{guess_count}次猜测（还剩{remaining}次机会）: ").strip()
                
                # 检查是否退出
                if user_input.lower() == 'q':
                    print("👋 游戏已退出！")
                    return
                
                # 检查是否为空
                if not user_input:
                    print("❌ 请输入一个数字！")
                    guess_count -= 1
                    continue
                
                guess = int(user_input)
                
                if guess < 1 or guess > 100:
                    print("❌ 请输入1到100之间的数字！")
                    guess_count -= 1
                    continue
                
                # 智能提示
                hint = self.get_smart_hint(guess, number, guess_count)
                print(f"💡 {hint}")
                
                if guess == number:
                    end_time = time.time()
                    game_time = end_time - start_time
                    game_won = True
                    
                    print(f"\n🎉 恭喜你猜对了！数字是{number}")
                    print(f"⏱️ 用时：{game_time:.1f}秒")
                    
                    # 等级评价
                    if guess_count == 1:
                        print("🏆 等级：神级！一次就猜中！")
                    elif guess_count <= 3:
                        print("👑 等级：大师级！非常厉害！")
                    elif guess_count <= 5:
                        print("⭐ 等级：专家级！表现不错！")
                    elif guess_count <= 7:
                        print("👍 等级：熟练级！还可以！")
                    elif guess_count <= 10:
                        print("🌱 等级：新手级！继续努力！")
                    
                    break
                    
                elif guess < number:
                    print("📈 猜小了")
                else:
                    print("📉 猜大了")
                    
            except ValueError:
                print("❌ 请输入有效的数字！")
                guess_count -= 1
                continue
        
        # 游戏结束处理
        if not game_won:
            print(f"\n😔 游戏结束！正确答案是{number}")
            print("🌱 等级：菜鸟级！需要多加练习！")
            game_time = time.time() - start_time
        
        # 记录游戏
        game_record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'attempts': guess_count,
            'time': game_time,
            'won': game_won,
            'number': number
        }
        self.game_history.append(game_record)
        self.update_stats(guess_count, game_won)
        self.check_achievements(guess_count, game_won)
        
        # 询问是否继续
        input("\n按回车键返回主菜单...")

def main():
    game = SmartGuessGame()
    
    while True:
        game.clear_screen()
        print("🎮 智能猜数字游戏")
        print("=" * 50)
        print("1. 开始游戏")
        print("2. 查看统计")
        print("3. 查看成就")
        print("4. 查看历史记录")
        print("5. 退出游戏")
        print("=" * 50)
        
        try:
            choice = input("请选择功能 (1-5): ").strip()
            
            if choice == "1":
                game.clear_screen()
                game.play_game()
            elif choice == "2":
                game.show_stats()
                input("\n按回车键返回主菜单...")
            elif choice == "3":
                game.show_achievements()
                input("\n按回车键返回主菜单...")
            elif choice == "4":
                game.show_history()
                input("\n按回车键返回主菜单...")
            elif choice == "5":
                print("👋 感谢游玩！再见！")
                break
            elif choice == "":
                print("❌ 请输入一个选项！")
                input("按回车键继续...")
            else:
                print("❌ 无效选择，请输入1-5之间的数字！")
                input("按回车键继续...")
                
        except KeyboardInterrupt:
            print("\n\n👋 游戏被中断，再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误：{e}")
            input("按回车键继续...")

if __name__ == "__main__":
    main()