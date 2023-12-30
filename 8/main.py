from datetime import date, datetime, timedelta



def get_birthdays_per_week(users):
    birthdays_per_week = {}    # Створення словника для зберігання днів народження на тиждень

    if not users:
        return birthdays_per_week
    
    if users:
        for user in users:
            name = user['name']
            birthday = user['birthday']
            current_date = date.today() 
            user_birthday = birthday.replace(year=current_date.year)
            day_of_week = user_birthday.strftime('%A') # День тижня
            delta_days = user_birthday - current_date
            interval = timedelta(days=7) # Інтервал перед днем народження (7 днів)
            
            if delta_days.days < 0: # коли всі дні народження користувачів вже минули у цьому році
                if birthday.replace(year=current_date.year + 1) <= current_date + interval: # День народження був протягом останніх 7 днів
                    if day_of_week == 'Saturday' or day_of_week == 'Sunday':
                        if 'Monday' not in birthdays_per_week:
                            birthdays_per_week['Monday'] = [name]
                        else:
                            birthdays_per_week['Monday'].append(name)
                
            else:       
                if day_of_week == 'Saturday' or day_of_week == 'Sunday':
                    if 'Monday' not in birthdays_per_week:
                        birthdays_per_week['Monday'] = [name]
                    else:
                        birthdays_per_week['Monday'].append(name)
                else: 
                    birthdays_per_week[day_of_week] = [name]
   
                
    #print('birthdays_per_week', birthdays_per_week)
    return birthdays_per_week
    

    

    

if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
