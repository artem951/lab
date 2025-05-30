import random
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QLabel, QVBoxLayout, QHBoxLayout, QWidget,
                             QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QPen
from itertools import combinations
from datetime import datetime


class CardWidget(QLabel):
    def __init__(self, card, parent=None):
        super().__init__(parent)
        self.card = card
        self.setFixedSize(80, 120)
        self.setStyleSheet("background-color: white; border-radius: 5px; border: 1px solid black;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor(255, 255, 255))

        if self.card[-1] in ['H', 'D']:
            color = QColor(255, 0, 0)
        else:
            color = QColor(0, 0, 0)

        painter.setPen(QPen(color, 2))

        rank = self.card[0]
        font = QFont('Arial', 20)
        painter.setFont(font)
        painter.drawText(10, 25, rank)

        suit = self.card[1]
        suit_symbol = ''
        if suit == 'H':
            suit_symbol = '♥'
        elif suit == 'D':
            suit_symbol = '♦'
        elif suit == 'C':
            suit_symbol = '♣'
        elif suit == 'S':
            suit_symbol = '♠'

        font = QFont('Arial', 24)
        painter.setFont(font)
        painter.drawText(10, 55, suit_symbol)

        if self.card == 'back':
            painter.fillRect(self.rect(), QColor(70, 130, 180))
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            font = QFont('Arial', 12)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, "X")


class PokerGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initGame()

    def initUI(self):
        self.setWindowTitle("Покер")
        self.setFixedSize(1400, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.info_label = QLabel("Покер")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setFont(QFont('Arial', 14))
        main_layout.addWidget(self.info_label)

        self.community_label = QLabel("Карты стола: ")
        self.community_label.setAlignment(Qt.AlignCenter)
        self.community_label.setFont(QFont('Arial', 12))
        self.community_cards_display = QHBoxLayout()
        self.community_cards_display.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.community_label)
        main_layout.addLayout(self.community_cards_display)

        players_layout = QHBoxLayout()

        self.bot1_group = QVBoxLayout()
        self.bot1_label = QLabel("Вова1")
        self.bot1_label.setAlignment(Qt.AlignCenter)
        self.bot1_stack_label = QLabel("Фишки: 1000")
        self.bot1_stack_label.setAlignment(Qt.AlignCenter)
        self.bot1_cards = QHBoxLayout()
        self.bot1_cards.setAlignment(Qt.AlignCenter)
        self.bot1_status = QLabel("Играет")
        self.bot1_status.setAlignment(Qt.AlignCenter)

        self.bot1_group.addWidget(self.bot1_label)
        self.bot1_group.addWidget(self.bot1_stack_label)
        self.bot1_group.addLayout(self.bot1_cards)
        self.bot1_group.addWidget(self.bot1_status)
        players_layout.addLayout(self.bot1_group)

        self.player_group = QVBoxLayout()
        self.player_label = QLabel("Вы")
        self.player_label.setAlignment(Qt.AlignCenter)
        self.player_stack_label = QLabel("Фишки: 1000")
        self.player_stack_label.setAlignment(Qt.AlignCenter)
        self.player_cards = QHBoxLayout()
        self.player_cards.setAlignment(Qt.AlignCenter)

        self.player_group.addWidget(self.player_label)
        self.player_group.addWidget(self.player_stack_label)
        self.player_group.addLayout(self.player_cards)
        players_layout.addLayout(self.player_group)

        self.bot2_group = QVBoxLayout()
        self.bot2_label = QLabel("Вова2")
        self.bot2_label.setAlignment(Qt.AlignCenter)
        self.bot2_stack_label = QLabel("Фишки: 1000")
        self.bot2_stack_label.setAlignment(Qt.AlignCenter)
        self.bot2_cards = QHBoxLayout()
        self.bot2_cards.setAlignment(Qt.AlignCenter)
        self.bot2_status = QLabel("Играет")
        self.bot2_status.setAlignment(Qt.AlignCenter)

        self.bot2_group.addWidget(self.bot2_label)
        self.bot2_group.addWidget(self.bot2_stack_label)
        self.bot2_group.addLayout(self.bot2_cards)
        self.bot2_group.addWidget(self.bot2_status)
        players_layout.addLayout(self.bot2_group)

        main_layout.addLayout(players_layout)

        self.pot_label = QLabel("Банк: 0")
        self.pot_label.setAlignment(Qt.AlignCenter)
        self.pot_label.setFont(QFont('Arial', 14))
        self.current_bet_label = QLabel("Текущая ставка: 0")
        self.current_bet_label.setAlignment(Qt.AlignCenter)
        self.current_bet_label.setFont(QFont('Arial', 12))

        main_layout.addWidget(self.pot_label)
        main_layout.addWidget(self.current_bet_label)

        # Action buttons
        buttons_layout = QHBoxLayout()

        self.fold_button = QPushButton("Сбросить")
        self.fold_button.setFixedSize(QSize(100, 50))
        self.fold_button.clicked.connect(self.fold)

        self.call_button = QPushButton("Колл (0)")
        self.call_button.setFixedSize(QSize(100, 50))
        self.call_button.clicked.connect(self.call)

        self.raise_button = QPushButton("Поднять")
        self.raise_button.setFixedSize(QSize(100, 50))
        self.raise_button.clicked.connect(self.raise_bet)

        self.raise_amount = QSpinBox()
        self.raise_amount.setRange(10, 1000)
        self.raise_amount.setSingleStep(10)
        self.raise_amount.setValue(20)
        self.raise_amount.setFixedSize(QSize(100, 50))

        buttons_layout.addWidget(self.fold_button)
        buttons_layout.addWidget(self.call_button)
        buttons_layout.addWidget(self.raise_button)
        buttons_layout.addWidget(self.raise_amount)

        main_layout.addLayout(buttons_layout)

        self.next_round_button = QPushButton("Следующий раунд")
        self.next_round_button.setFixedSize(QSize(200, 50))
        self.next_round_button.clicked.connect(self.next_round)
        self.next_round_button.hide()
        main_layout.addWidget(self.next_round_button, alignment=Qt.AlignCenter)

        self.leaderboard_button = QPushButton("Таблица лидеров")
        self.leaderboard_button.setFixedSize(QSize(200, 50))
        self.leaderboard_button.clicked.connect(self.show_leaderboard)
        main_layout.addWidget(self.leaderboard_button, alignment=Qt.AlignCenter)

    def initGame(self):
        self.deck = [r + s for r in '23456789TJQKA' for s in 'CDHS']
        random.shuffle(self.deck)

        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.bot1_hand = [self.deck.pop(), self.deck.pop()]
        self.bot2_hand = [self.deck.pop(), self.deck.pop()]
        self.community_cards = []

        self.player_stack_value = 1000
        self.bot1_stack_value = 1000
        self.bot2_stack_value = 1000

        self.pot = 0
        self.current_bet = 0
        self.round_stage = 0

        self.folded = {'player': False, 'bot1': False, 'bot2': False}
        self.game_over = False

        self.updateUI()

    def updateUI(self):
        self.player_stack_label.setText(f"Фишки: {self.player_stack_value}")
        self.bot1_stack_label.setText(f"Фишки: {self.bot1_stack_value}")
        self.bot2_stack_label.setText(f"Фишки: {self.bot2_stack_value}")

        self.pot_label.setText(f"Банк: {self.pot}")
        self.current_bet_label.setText(f"Текущая ставка: {self.current_bet}")
        self.call_button.setText(f"Колл ({min(self.current_bet, self.player_stack_value)})")

        self.updateCardsDisplay()

        self.bot1_status.setText("Сбросил" if self.folded['bot1'] else "Играет")
        self.bot2_status.setText("Сбросил" if self.folded['bot2'] else "Играет")

        self.updateCommunityCards()

        self.updateButtonStates()

    def updateCardsDisplay(self):
        for i in reversed(range(self.player_cards.count())):
            self.player_cards.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.bot1_cards.count())):
            self.bot1_cards.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.bot2_cards.count())):
            self.bot2_cards.itemAt(i).widget().deleteLater()

        for card in self.player_hand:
            card_widget = CardWidget(card)
            self.player_cards.addWidget(card_widget)

        for card in self.bot1_hand:
            if self.folded['bot1'] or self.game_over or self.round_stage == 3:
                card_widget = CardWidget(card)
            else:
                card_widget = CardWidget('back')
            self.bot1_cards.addWidget(card_widget)

        for card in self.bot2_hand:
            if self.folded['bot2'] or self.game_over or self.round_stage == 3:
                card_widget = CardWidget(card)
            else:
                card_widget = CardWidget('back')
            self.bot2_cards.addWidget(card_widget)

    def updateCommunityCards(self):
        for i in reversed(range(self.community_cards_display.count())):
            self.community_cards_display.itemAt(i).widget().deleteLater()

        for card in self.community_cards:
            card_widget = CardWidget(card)
            self.community_cards_display.addWidget(card_widget)

    def updateButtonStates(self):
        if self.folded['player'] or self.game_over:
            self.fold_button.setEnabled(False)
            self.call_button.setEnabled(False)
            self.raise_button.setEnabled(False)
            self.raise_amount.setEnabled(False)
        else:
            self.fold_button.setEnabled(True)
            self.call_button.setEnabled(True)
            self.raise_button.setEnabled(True)
            self.raise_amount.setEnabled(True)

        if self.current_bet == 0 or self.player_stack_value == 0:
            self.call_button.setEnabled(False)
        else:
            self.call_button.setEnabled(True)

        if self.player_stack_value <= self.current_bet:
            self.raise_button.setEnabled(False)
            self.raise_amount.setEnabled(False)

    def fold(self):
        self.folded['player'] = True
        self.info_label.setText("Вы сбросили карты!")
        self.updateUI()
        self.botActions()
        self.checkRoundEnd()

    def call(self):
        call_amount = min(self.current_bet, self.player_stack_value)
        self.player_stack_value -= call_amount
        self.pot += call_amount
        self.info_label.setText(f"Вы уравняли ставку {call_amount}")
        self.updateUI()
        self.botActions()
        self.checkRoundEnd()

    def raise_bet(self):
        raise_amount = self.raise_amount.value()
        total_bet = self.current_bet + raise_amount

        if total_bet > self.player_stack_value:
            total_bet = self.player_stack_value
            raise_amount = total_bet - self.current_bet

        self.current_bet = total_bet
        self.player_stack_value -= total_bet
        self.pot += total_bet
        self.info_label.setText(f"Вы повысили ставку до {total_bet}")
        self.updateUI()
        self.botActions()
        self.checkRoundEnd()

    def botActions(self):
        if not self.folded['bot1']:
            if random.random() < 0.1:
                self.folded['bot1'] = True
                self.info_label.setText(self.info_label.text() + "\nБот 1 сбросил карты!")
            else:
                if random.random() < 0.3 and self.bot1_stack_value > self.current_bet:  # 30% chance to raise
                    raise_amount = random.randint(10, min(100, self.bot1_stack_value - self.current_bet))
                    self.current_bet += raise_amount
                    self.bot1_stack_value -= self.current_bet
                    self.pot += self.current_bet
                    self.info_label.setText(self.info_label.text() + f"\nБот 1 повысил ставку до {self.current_bet}!")
                else:  # Call
                    call_amount = min(self.current_bet, self.bot1_stack_value)
                    self.bot1_stack_value -= call_amount
                    self.pot += call_amount
                    if call_amount > 0:
                        self.info_label.setText(self.info_label.text() + f"\nБот 1 уравнял ставку {call_amount}")

        # Bot 2 action
        if not self.folded['bot2']:
            if random.random() < 0.1:
                self.folded['bot2'] = True
                self.info_label.setText(self.info_label.text() + "\nБот 2 сбросил карты!")
            else:
                if random.random() < 0.3 and self.bot2_stack_value > self.current_bet:  # 30% chance to raise
                    raise_amount = random.randint(10, min(100, self.bot2_stack_value - self.current_bet))
                    self.current_bet += raise_amount
                    self.bot2_stack_value -= self.current_bet
                    self.pot += self.current_bet
                    self.info_label.setText(self.info_label.text() + f"\nБот 2 повысил ставку до {self.current_bet}!")
                else:  # Call
                    call_amount = min(self.current_bet, self.bot2_stack_value)
                    self.bot2_stack_value -= call_amount
                    self.pot += call_amount
                    if call_amount > 0:
                        self.info_label.setText(self.info_label.text() + f"\nБот 2 уравнял ставку {call_amount}")

        self.updateUI()

    def evaluate_hand(self, hand, community):
        all_cards = hand + community
        best_rank = (10, None)
        hand_name = ""

        rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                    '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        for combo in combinations(all_cards, 5):
            ranks = sorted([rank_map[card[0]] for card in combo], reverse=True)
            suits = [card[1] for card in combo]

            is_flush = len(set(suits)) == 1

            is_straight = False
            if max(ranks) - min(ranks) == 4 and len(set(ranks)) == 5:
                is_straight = True
            if ranks == [14, 5, 4, 3, 2]:
                is_straight = True
                ranks = [5, 4, 3, 2, 1]

            rank_counts = {}
            for rank in ranks:
                rank_counts[rank] = rank_counts.get(rank, 0) + 1

            # Get pairs, three of a kind, etc.
            pairs = [r for r, c in rank_counts.items() if c == 2]
            triples = [r for r, c in rank_counts.items() if c == 3]
            quads = [r for r, c in rank_counts.items() if c == 4]

            # Hand rankings (lower is better):
            # 0: Royal Flush, 1: Straight Flush, 2: Four of a Kind, 3: Full House
            # 4: Flush, 5: Straight, 6: Three of a Kind, 7: Two Pair, 8: Pair, 9: High Card

            if is_flush and is_straight and ranks[0] == 14:
                # Royal Flush
                if best_rank[0] > 0:
                    best_rank = (0, ranks)
                    hand_name = "Роял Флеш"
            elif is_flush and is_straight:
                # Straight Flush
                if best_rank[0] > 1:
                    best_rank = (1, ranks)
                    hand_name = f"Стрит Флеш (от {ranks[0]})"
            elif quads:
                # Four of a Kind
                kickers = [r for r in ranks if r != quads[0]]
                if best_rank[0] > 2 or (best_rank[0] == 2 and quads[0] > best_rank[1][0]):
                    best_rank = (2, [quads[0]] + kickers)
                    hand_name = f"Каре ({quads[0]})"
            elif triples and pairs:
                # Full House
                if best_rank[0] > 3 or (best_rank[0] == 3 and triples[0] > best_rank[1][0]):
                    best_rank = (3, [triples[0], pairs[0]])
                    hand_name = f"Фул Хаус ({triples[0]} над {pairs[0]})"
            elif is_flush:
                # Flush
                if best_rank[0] > 4:
                    best_rank = (4, ranks)
                    hand_name = f"Флеш (старшая {ranks[0]})"
            elif is_straight:
                # Straight
                if best_rank[0] > 5:
                    best_rank = (5, ranks)
                    hand_name = f"Стрит (от {ranks[0]})"
            elif triples:
                # Three of a Kind
                kickers = [r for r in ranks if r != triples[0]]
                if best_rank[0] > 6 or (best_rank[0] == 6 and triples[0] > best_rank[1][0]):
                    best_rank = (6, [triples[0]] + kickers)
                    hand_name = f"Тройка ({triples[0]})"
            elif len(pairs) >= 2:
                # Two Pair
                pairs = sorted(pairs, reverse=True)[:2]
                kickers = [r for r in ranks if r not in pairs]
                if best_rank[0] > 7 or (best_rank[0] == 7 and (pairs[0] > best_rank[1][0] or
                                                               (pairs[0] == best_rank[1][0] and pairs[1] > best_rank[1][
                                                                   1]))):
                    best_rank = (7, pairs + kickers)
                    hand_name = f"Две Пары ({pairs[0]}, {pairs[1]})"
            elif pairs:
                # Pair
                kickers = [r for r in ranks if r != pairs[0]]
                if best_rank[0] > 8 or (best_rank[0] == 8 and pairs[0] > best_rank[1][0]):
                    best_rank = (8, [pairs[0]] + kickers)
                    hand_name = f"Пара ({pairs[0]})"
            else:
                # High Card
                if best_rank[0] > 9 or (best_rank[0] == 9 and ranks > best_rank[1]):
                    best_rank = (9, ranks)
                    hand_name = f"Старшая карта ({ranks[0]})"

        return best_rank, hand_name

    def checkRoundEnd(self):
        # Check if all players have acted
        active_players = [name for name, folded in self.folded.items() if not folded]

        # If only one player remains, they win
        if len(active_players) == 1:
            self.endGame(active_players[0])
            return

        # If all players have called the current bet (or folded), proceed to next stage
        if (self.round_stage == 0 and len(self.community_cards) == 0) or \
                (self.round_stage == 1 and len(self.community_cards) == 3) or \
                (self.round_stage == 2 and len(self.community_cards) == 4):

            self.current_bet = 0
            self.round_stage += 1

            if self.round_stage == 1:  # Flop
                self.community_cards.extend([self.deck.pop(), self.deck.pop(), self.deck.pop()])
                self.info_label.setText("Флоп открыт!")
            elif self.round_stage == 2:  # Turn
                self.community_cards.append(self.deck.pop())
                self.info_label.setText("Терн открыт!")
            elif self.round_stage == 3:  # River
                self.community_cards.append(self.deck.pop())
                self.info_label.setText("Ривер открыт! Вскрытие карт!")
                self.endGame()  # End game immediately after river
                return

            self.updateUI()

    def endGame(self, winner=None):
        self.game_over = True
        self.next_round_button.show()

        if winner:
            # Single winner case (someone folded)
            if winner == 'player':
                self.player_stack_value += self.pot
                message = f"Вы выиграли {self.pot} фишек!"
                self.save_result("Игрок", self.pot)
            elif winner == 'bot1':
                self.bot1_stack_value += self.pot
                message = "Бот 1 выиграл!"
                self.save_result("Бот 1", self.pot)
            else:
                self.bot2_stack_value += self.pot
                message = "Бот 2 выиграл!"
                self.save_result("Бот 2", self.pot)
        else:
            active_players = [name for name, folded in self.folded.items() if not folded]
            if active_players:
                hands = {
                    'player': self.evaluate_hand(self.player_hand, self.community_cards),
                    'bot1': self.evaluate_hand(self.bot1_hand, self.community_cards) if not self.folded['bot1'] else (
                    11, None),
                    'bot2': self.evaluate_hand(self.bot2_hand, self.community_cards) if not self.folded['bot2'] else (
                    11, None)
                }

                best_rank = min(hands.values(), key=lambda x: (x[0], x[1] if x[1] else [0]))
                winners = [(name, hand[1]) for name, hand in hands.items() if
                           hand[0] == best_rank[0] and hand[1] == best_rank[1]]

                # If multiple players have the same hand rank, split the pot
                pot_per_winner = self.pot // len(winners)
                winner_names = []
                for name, hand_name in winners:
                    if name == 'player':
                        self.player_stack_value += pot_per_winner
                        winner_names.append(f"Вы ({hand_name})")
                        self.save_result("Игрок", pot_per_winner)
                    elif name == 'bot1':
                        self.bot1_stack_value += pot_per_winner
                        winner_names.append(f"Вова1 ({hand_name})")
                        self.save_result("Вова1", pot_per_winner)
                    else:
                        self.bot2_stack_value += pot_per_winner
                        winner_names.append(f"Вова      2 ({hand_name})")
                        self.save_result("Вова2", pot_per_winner)

                message = f"Победители: {', '.join(winner_names)}! он получает {pot_per_winner} фишек!"
            else:
                message = "Все игроки сбросили карты! Банк возвращается."

        self.info_label.setText(f"Игра окончена! {message}")
        self.updateUI()

        if self.player_stack_value == 0:
            QMessageBox.information(self, "Конец игры", "У вас закончились фишки! Игра окончена.")
            self.close()
        elif self.bot1_stack_value == 0:
            QMessageBox.information(self, "Конец игры", "У Бота 1 закончились фишки!")
        elif self.bot2_stack_value == 0:
            QMessageBox.information(self, "Конец игры", "У Бота 2 закончились фишки!")

    def save_result(self, winner_name, chips_won):
        try:
            with open("lider.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - {winner_name} выиграл {chips_won} фишек\n")
        except Exception as e:
            print(f"Ошибка при сохранении результата: {e}")

    def show_leaderboard(self):
        try:
            with open("lider.txt", "r", encoding="utf-8") as f:
                leaderboard = f.read()
        except FileNotFoundError:
            leaderboard = "Таблица лидеров пуста."
        except Exception as e:
            leaderboard = f"Ошибка при чтении таблицы лидеров: {e}"

        msg = QMessageBox()
        msg.setWindowTitle("Таблица лидеров")
        msg.setText(leaderboard)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def next_round(self):
        self.next_round_button.hide()
        self.initGame()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = PokerGame()
    game.show()
    sys.exit(app.exec_())
