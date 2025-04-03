# Крестики-Нолики для Android

Простая и увлекательная игра "Крестики-Нолики" с красивым интерфейсом и возможностью игры против компьютера.

## Особенности приложения

- Интуитивно понятный пользовательский интерфейс
- Возможность игры против компьютера или с другом
- Адаптивный искусственный интеллект
- Анимации для улучшения пользовательского опыта
- Поддержка русского языка

## Скриншоты

*Здесь будут размещены скриншоты приложения*

## Сборка приложения для Android

### Требования

- Python 3.8 или выше
- [Buildozer](https://github.com/kivy/buildozer)
- [Android SDK](https://developer.android.com/studio)
- [Java JDK](https://openjdk.java.net/)
- [Android NDK](https://developer.android.com/ndk/)

### Шаги по сборке APK

1. Установите все необходимые зависимости:

```bash
pip install kivy buildozer
```

2. Инициализируйте проект Buildozer (уже сделано в этом репозитории):

```bash
buildozer init
```

3. Настройте файл `buildozer.spec` под свои нужды (уже настроен в этом репозитории).

4. Соберите APK:

```bash
buildozer -v android debug
```

После успешной сборки файл APK будет находиться в директории `bin/`.

### Установка на устройство

```bash
buildozer android deploy run
```

## Публикация в Google Play

1. Создайте аккаунт разработчика Google Play (платно, $25).
2. Соберите релизную версию APK:

```bash
buildozer android release
```

3. Подпишите APK с помощью keystore:

```bash
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore bin/tictactoe-*-release-unsigned.apk alias_name
```

4. Оптимизируйте APK:

```bash
$ANDROID_HOME/build-tools/<version>/zipalign -v 4 bin/tictactoe-*-release-unsigned.apk bin/tictactoe.apk
```

5. Загрузите подписанный APK через [Google Play Console](https://play.google.com/console/).

6. Заполните все необходимые метаданные:
   - Описание приложения
   - Скриншоты
   - Иконка
   - Бюджет и ценообразование
   - Ограничения по возрасту
   - Политика конфиденциальности

7. Отправьте приложение на проверку.

## Лицензия

MIT

## Автор

Ваше имя