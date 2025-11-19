"""
Smart Home Automation with NLP - University Project
Simple Python implementation demonstrating:
- Smart home device automation
- Rule-based system
- Basic NLP processing
- Natural language to automation rules
"""
 
import re
import json
from datetime import datetime
import time
 
class SmartHomeSystem:
    def __init__(self):
        # Device states
        self.devices = {
            'lights': False,
            'ac': False,
            'heating': False,
            'security': False,
            'temperature': 22,
            'motion': False,
            'time': '17:00'
        }
       
        # Automation rules
        self.rules = [
            'IF temperature > 25 THEN turn on ac',
            'IF motion detected THEN turn on security',
            'IF time is 18:00 THEN turn on lights'
        ]
       
        print("🏠 Smart Home System Initialized")
        print("=" * 50)
 
    def parse_rule(self, rule):
        """Parse automation rule into conditions and actions"""
        conditions = []
        actions = []

        # Extract temperature comparisons
        temp_patterns = [
            (r'temperature > (\d+)', '>', int),
            (r'temperature < (\d+)', '<', int),
            (r'temperature >= (\d+)', '>=', int),
            (r'temperature <= (\d+)', '<=', int)
        ]
        for pattern, operator, cast in temp_patterns:
            match = re.search(pattern, rule)
            if match:
                conditions.append({
                    'type': 'temp',
                    'value': cast(match.group(1)),
                    'operator': operator
                })

        # Time condition
        if 'time is' in rule:
            match = re.search(r'time is (\d{2}:\d{2})', rule)
            if match:
                conditions.append({
                    'type': 'time',
                    'value': match.group(1),
                    'operator': '=='
                })

        # Motion detection
        if 'motion detected' in rule:
            conditions.append({'type': 'motion', 'value': True})

        # Extract actions
        action_patterns = {
            'turn on lights': ('lights', True),
            'turn off lights': ('lights', False),
            'turn on ac': ('ac', True),
            'turn off ac': ('ac', False),
            'turn on heating': ('heating', True),
            'turn off heating': ('heating', False),
            'turn on security': ('security', True),
            'turn off security': ('security', False),
            'turn on motion': ('motion', True),
            'turn off motion': ('motion', False)
        }
        for key, (device, state) in action_patterns.items():
            if key in rule:
                actions.append({'device': device, 'state': state})

        return conditions, actions

 
    def execute_rules(self):
        """Execute all automation rules"""
        executed_rules = []
       
        for rule in self.rules:
            conditions, actions = self.parse_rule(rule)
            should_execute = True
           
            # Check all conditions
            for condition in conditions:
                if condition['type'] == 'temp':
                    device_temp = self.devices['temperature']
                    operator = condition['operator']
                    value = condition['value']
                    if operator == '>' and not (device_temp > value):
                        should_execute = False
                    elif operator == '<' and not (device_temp < value):
                        should_execute = False
                    elif operator == '>=' and not (device_temp >= value):
                        should_execute = False
                    elif operator == '<=' and not (device_temp <= value):
                        should_execute = False
                elif condition['type'] == 'time':
                    if self.devices['time'] != condition['value']:
                        should_execute = False
                elif condition['type'] == 'motion':
                    if self.devices['motion'] != condition['value']:
                        should_execute = False
           
            # Execute actions if conditions met
            if should_execute and actions:
                for action in actions:
                    old_state = self.devices[action['device']]
                    self.devices[action['device']] = action['state']
                    if old_state != action['state']:
                        executed_rules.append(f"✓ {rule}")
                        print(f"🔧 Executed: {action['device']} → {'ON' if action['state'] else 'OFF'}")
       
        return executed_rules
 
    def display_status(self):
        """Display current device status"""
        print("\n📊 DEVICE STATUS:")
        print("-" * 30)
        for device, state in self.devices.items():
            if device in ['temperature', 'time']:
                unit = '°C' if device == 'temperature' else ''
                print(f"{device.capitalize()}: {state}{unit}")
            else:
                status = '🟢 ON' if state else '🔴 OFF'
                print(f"{device.capitalize()}: {status}")
 
    def add_rule(self, rule):
        """Add new automation rule"""
        if rule and rule not in self.rules:
            self.rules.append(rule)
            print(f"✅ Rule added: {rule}")
        else:
            print("❌ Invalid or duplicate rule")
 
    def remove_rule(self, index):
        """Remove automation rule by index"""
        if 0 <= index < len(self.rules):
            removed = self.rules.pop(index)
            print(f"🗑️ Rule removed: {removed}")
        else:
            print("❌ Invalid rule index")
 
    def list_rules(self):
        """Display all automation rules"""
        print("\n📋 AUTOMATION RULES:")
        print("-" * 40)
        for i, rule in enumerate(self.rules):
            print(f"{i+1}. {rule}")
 
class NLPProcessor:

    def natural_language_to_rule(self, text):
        """Convert natural language to automation rule or direct command"""
        text_lower = text.lower()
        conditions = []
        actions = []
        direct_commands = []

        # Temperature conditions
        if re.search(r'\b(hot|warm)\b', text_lower):
            conditions.append('temperature > 25')
        elif re.search(r'\b(cold|cool|chilly)\b', text_lower):
            conditions.append('temperature < 18')
        elif 'comfortable' in text_lower or 'normal temperature' in text_lower:
            conditions.append('temperature >= 18 AND temperature <= 22')

        # Time conditions (intervals)
        if any(word in text_lower for word in ['in the evening', 'evening', 'at night', 'dark']):
            if 'time >= 18:00 AND time < 22:00' not in conditions:
                conditions.append('time >= 18:00 AND time < 22:00')

        if any(word in text_lower for word in ['morning', 'in the morning', 'dawn']):
            if 'time >= 06:00 AND time < 10:00' not in conditions:
                conditions.append('time >= 06:00 AND time < 10:00')

        if any(word in text_lower for word in ['afternoon', 'in the afternoon']):
            if 'time >= 12:00 AND time < 18:00' not in conditions:
                conditions.append('time >= 12:00 AND time < 18:00')

        # Motion detection
        if any(word in text_lower for word in ['motion', 'movement', 'detect']):
            if 'motion detected' not in conditions:
                conditions.append('motion detected')

        # Direct commands (set time/temperature)
        match_time = re.search(r'set time to (\d{1,2}:\d{2})', text_lower)
        if match_time:
            direct_commands.append(f"set time to {match_time.group(1)}")

        match_temp = re.search(r'set temperature to (\d+)', text_lower)
        if match_temp:
            direct_commands.append(f"set temperature to {match_temp.group(1)}")

        # Device action mappings
        action_map = {
            'lights': ['light', 'lights'],
            'ac': ['ac', 'air conditioning', 'cooling'],
            'heating': ['heating', 'heater'],
            'security': ['security', 'alarm', 'security system'],
            'motion': ['motion', 'motion detection', 'motion sensor', 'movement']
        }


        for device, keywords in action_map.items():
            for keyword in keywords:
                if any(f in text_lower for f in [f'turn on {keyword}', f'enable {keyword}', f'activate {keyword}', f'start {keyword}']):
                    actions.append(f'turn on {device}')
                if any(f in text_lower for f in [f'turn off {keyword}', f'disable {keyword}', f'deactivate {keyword}', f'stop {keyword}']):
                    actions.append(f'turn off {device}')

        # Determine if it's a rule or command
        if (('if' in text_lower or 'when' in text_lower or any(t in text_lower for t in ['morning', 'evening', 'afternoon', 'night'])) and conditions and actions):
            rule = 'IF ' + ' AND '.join(conditions) + ' THEN ' + ' AND '.join(actions)
            return rule.strip()

        # Otherwise, treat as direct command
        if direct_commands or actions:
            return ' AND '.join(direct_commands + actions)

        return 'Could not parse command'


def main():
    # Initialize systems
    smart_home = SmartHomeSystem()
    nlp = NLPProcessor()
   
    def print_menu():
        print("\n" + "="*50)
        print("🏠 SMART HOME CONTROL MENU")
        print("="*50)
        print("1. Show device status")
        print("2. Control devices manually")
        print("3. Show automation rules")
        print("4. Add automation rule")
        print("5. Remove automation rule")
        print("6. Natural language command")
        print("7. Run automation demo")
        print("8. Exit")
        print("-"*50)
 
    def manual_control():
        print("\n🎛️ MANUAL DEVICE CONTROL:")
        print("1. Set temperature")
        print("2. Set time")
        print("3. Toggle motion detection")
        print("4. Toggle lights")
        print("5. Toggle AC")
       
        choice = input("Select option (1-5): ").strip()
       
        if choice == '1':
            try:
                temp = int(input("Enter temperature (15-35°C): "))
                if 15 <= temp <= 35:
                    smart_home.devices['temperature'] = temp
                    print(f"🌡️ Temperature set to {temp}°C")
                    smart_home.execute_rules()
                else:
                    print("❌ Temperature must be between 15-35°C")
            except ValueError:
                print("❌ Invalid temperature value")
       
        elif choice == '2':
            time_input = input("Enter time (HH:MM): ").strip()
            if re.match(r'^\d{2}:\d{2}$', time_input):
                smart_home.devices['time'] = time_input
                print(f"🕐 Time set to {time_input}")
                smart_home.execute_rules()
            else:
                print("❌ Invalid time format (use HH:MM)")
       
        elif choice == '3':
            smart_home.devices['motion'] = not smart_home.devices['motion']
            status = 'DETECTED' if smart_home.devices['motion'] else 'NONE'
            print(f"👁️ Motion detection: {status}")
            smart_home.execute_rules()
       
        elif choice == '4':
            smart_home.devices['lights'] = not smart_home.devices['lights']
            status = 'ON' if smart_home.devices['lights'] else 'OFF'
            print(f"💡 Lights: {status}")
       
        elif choice == '5':
            smart_home.devices['ac'] = not smart_home.devices['ac']
            status = 'ON' if smart_home.devices['ac'] else 'OFF'
            print(f"❄️ AC: {status}")
 
 
    def natural_language_command():
        print("\n🗣️ NATURAL LANGUAGE COMMAND:")
        print("Examples:")
        print("  • 'When it is hot turn on ac'")
        print("  • 'If motion detected turn on security'")
        print("  • 'In the evening turn on lights'")
        print("  • 'Turn off lights'")
        print("  • 'Set temperature to 20'")
        print("  • 'Disable motion detection'")
    
        command = input("\nEnter command: ").strip()

        if not command:
            print("❌ Please enter a command")
            return

        rule = nlp.natural_language_to_rule(command)
        print(f"\n🔄 Parsed: {rule}")

        # Dacă e regulă condiționată
        if 'if' in rule.lower() and 'then' in rule.lower():
            add_it = input("Add this rule to automation? (y/n): ").lower().strip()
            if add_it == 'y':
                smart_home.add_rule(rule)

        # Comenzi directe executate imediat
        elif rule != 'Could not parse command':
            print("⚙️ Executing direct command...")

            if 'set temperature to' in rule:
                match = re.search(r'set temperature to (\d+)', rule)
                if match:
                    temp = int(match.group(1))
                    smart_home.devices['temperature'] = temp
                    print(f"🌡️ Temperature set to {temp}°C")
                    smart_home.execute_rules()

            elif 'set time to' in rule:
                match = re.search(r'set time to (\d{1,2}:\d{2})', rule)
                if match:
                    smart_home.devices['time'] = match.group(1)
                    print(f"🕐 Time set to {match.group(1)}")
                    smart_home.execute_rules()

            else:
                # Comenzi directe: turn on/off/etc.
                normalized_rule = rule.replace('motion detection', 'motion') \
                      .replace('motion sensor', 'motion') \
                      .replace('security system', 'security')

                _, actions = smart_home.parse_rule(f"IF dummy THEN {normalized_rule}")
                for action in actions:
                    device = action['device']
                    state = action['state']
    
                    smart_home.devices[device] = state

                    if device == 'motion':
                        print(f"👁️ Motion detection: {'DETECTED' if state else 'NONE'}")
                    else:
                        print(f"🔧 Executed: {device} → {'ON' if state else 'OFF'}")
                
                    executed = smart_home.execute_rules()
                    for rule in executed:
                        print(f"🔄 Triggered by rule: {rule}")

        else:
            print("❌ Could not understand the command")

 
    def automation_demo():
        print("\n🎬 AUTOMATION DEMO:")
        print("Simulating different scenarios...")
       
        scenarios = [
            ("Setting temperature to 26°C (hot)", lambda: setattr(smart_home.devices, 'temperature', 26) or smart_home.__setitem__('temperature', 26)),
            ("Activating motion sensor", lambda: smart_home.devices.__setitem__('motion', True)),
            ("Setting time to 18:00 (evening)", lambda: smart_home.devices.__setitem__('time', '18:00'))
        ]
       
        for desc, action in scenarios:
            print(f"\n📌 {desc}")
            if 'temperature' in desc:
                smart_home.devices['temperature'] = 26
            elif 'motion' in desc:
                smart_home.devices['motion'] = True
            elif 'time' in desc:
                smart_home.devices['time'] = '18:00'
           
            executed = smart_home.execute_rules()
            if executed:
                for rule in executed:
                    print(f"   {rule}")
            else:
                print("   No rules triggered")
           
            smart_home.display_status()
            time.sleep(1)
 
    # Main program loop
    while True:
        try:
            print_menu()
            choice = input("Enter your choice (1-8): ").strip()
           
            if choice == '1':
                smart_home.display_status()
           
            elif choice == '2':
                manual_control()
           
            elif choice == '3':
                smart_home.list_rules()
           
            elif choice == '4':
                rule = input("Enter new rule (e.g., 'IF temperature > 25 THEN turn on ac'): ").strip()
                smart_home.add_rule(rule)
           
            elif choice == '5':
                smart_home.list_rules()
                try:
                    index = int(input("Enter rule number to remove: ")) - 1
                    smart_home.remove_rule(index)
                except ValueError:
                    print("❌ Invalid rule number")
           
            elif choice == '6':
                natural_language_command()
           
            elif choice == '7':
                automation_demo()
           
            elif choice == '8':
                print("👋 Goodbye! Smart Home System shutting down...")
                break
           
            else:
                print("❌ Invalid choice. Please enter 1-9.")
       
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
 
if __name__ == "__main__":
    print("🚀 Starting Smart Home Automation with NLP")
    print("University Project - Computer Science")
    main()