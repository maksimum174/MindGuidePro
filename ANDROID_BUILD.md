# Сборка и установка для Android

## Подробная инструкция по сборке APK

### Предварительные требования

Для успешной сборки APK на вашем компьютере должны быть установлены:

1. **Linux** или **macOS** (Windows поддерживается через WSL)
2. **Python 3.8+**
3. **Java JDK 8+**
4. **Buildozer** и его зависимости

### Установка необходимых зависимостей

#### На Ubuntu/Debian Linux:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-dev git zip unzip openjdk-8-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade buildozer Cython==0.29.19
```

#### На macOS:

```bash
brew install python3 git autoconf automake libtool pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer
pip3 install --user --upgrade buildozer Cython==0.29.19
```

### Процесс сборки

1. **Клонирование репозитория**

   ```bash
   git clone https://github.com/yourusername/tictactoe.git
   cd tictactoe
   ```

2. **Подготовка конфигурации Buildozer**

   Убедитесь, что файл `buildozer.spec` настроен правильно. Особое внимание обратите на следующие параметры:

   - `title`: название приложения
   - `package.name`: уникальное имя пакета
   - `package.domain`: домен разработчика
   - `android.permissions`: требуемые разрешения
   - `android.api`: целевая версия Android API
   - `android.minapi`: минимальная поддерживаемая версия Android API
   
   В нашем случае файл уже настроен для игры "Крестики-Нолики".

3. **Запуск сборки**

   ```bash
   buildozer android debug
   ```

   Примечание: первая сборка может занять длительное время (30+ минут), так как Buildozer загружает и устанавливает Android SDK, NDK и другие зависимости.

4. **Результат сборки**

   После успешной сборки вы найдете APK-файл в директории `./bin/`:
   ```
   ./bin/tictactoe-0.1-armeabi-v7a-debug.apk
   ```

### Установка на устройство Android

#### Метод 1: Через USB-кабель и ADB

1. Подключите ваше Android-устройство к компьютеру через USB
2. Включите "Режим разработчика" и "Отладку по USB" на устройстве
3. Установите ADB (Android Debug Bridge):
   ```bash
   # На Ubuntu/Debian
   sudo apt install android-tools-adb
   
   # На macOS
   brew install android-platform-tools
   ```
4. Проверьте соединение с устройством:
   ```bash
   adb devices
   ```
5. Установите APK на устройство:
   ```bash
   adb install -r ./bin/tictactoe-0.1-armeabi-v7a-debug.apk
   ```

#### Метод 2: Через передачу файла

1. Скопируйте APK-файл на ваше Android-устройство любым удобным способом (email, облачное хранилище, USB-кабель)
2. На устройстве откройте Файловый менеджер и найдите скопированный APK
3. Нажмите на файл для начала установки
4. Если появится предупреждение о безопасности, вам нужно разрешить установку из неизвестных источников:
   - Перейдите в Настройки > Безопасность > Неизвестные источники (на новых версиях Android этот параметр находится в Настройки > Приложения > Специальный доступ)
   - Включите опцию "Разрешить установку из этого источника"
5. Вернитесь к установке и завершите процесс

## Подписание APK для публикации в Google Play

Для публикации в Google Play требуется подписанный релиз-APK. Чтобы его создать:

1. **Создайте keystore файл** (если у вас его еще нет):
   ```bash
   keytool -genkey -v -keystore tictactoe.keystore -alias tictactoe -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **Настройте Buildozer для релизной сборки**, добавив в buildozer.spec:
   ```
   android.release_artifact = apk
   p4a.sign_with_cryptography = True
   android.keystore = tictactoe.keystore
   android.keyalias = tictactoe
   ```

3. **Создайте release-сборку**:
   ```bash
   buildozer android release
   ```

4. **Результат сборки**:
   После успешной сборки подписанный APK будет находиться в директории `./bin/`

## Требования к публикации в Google Play

Для публикации в Google Play вам потребуется:

1. Аккаунт разработчика Google Play (регистрация стоит $25)
2. Подписанный APK или App Bundle
3. Графические материалы:
   - Иконка приложения (512x512px)
   - Скриншоты приложения (минимум 2)
   - Полноэкранный баннер (1024x500px)
4. Текстовые материалы:
   - Название приложения
   - Краткое и полное описание
   - Категория и теги
   - Информация о политике конфиденциальности

## Устранение неполадок

### Проблемы при сборке

- **Ошибка "Error compiling"**: Убедитесь, что все зависимости установлены и у вас достаточно места на диске
- **Java-ошибки**: Проверьте, что установлена правильная версия JDK (8+)
- **Ошибки permissions**: Проверьте, что у вас есть права на запись в директорию проекта
- **Ошибки с NDK**: Иногда Buildozer не может автоматически загрузить NDK. Скачайте NDK вручную и укажите путь в buildozer.spec

### Проблемы при установке

- **"App not installed"**: Возможно, у вас уже установлена версия с таким же package name. Удалите ее перед установкой новой
- **"Parse error"**: APK-файл может быть поврежден или несовместим с вашим устройством
- **"Blocked by Play Protect"**: Нажмите "Установить все равно" или временно отключите Play Protect