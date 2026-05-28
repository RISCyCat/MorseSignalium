// MorseSignalium - C++ Console Version
// Author: RISCyCat
// Description: Educational Morse encoder and decoder implemented in C++17.

#include <algorithm>
#include <cctype>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>

using namespace std;

const unordered_map<char, string> MORSE_CODE = {
    {'A', ".-"}, {'B', "-..."}, {'C', "-.-."}, {'D', "-.."}, {'E', "."},
    {'F', "..-."}, {'G', "--."}, {'H', "...."}, {'I', ".."}, {'J', ".---"},
    {'K', "-.-"}, {'L', ".-.."}, {'M', "--"}, {'N', "-."}, {'O', "---"},
    {'P', ".--."}, {'Q', "--.-"}, {'R', ".-."}, {'S', "..."}, {'T', "-"},
    {'U', "..-"}, {'V', "...-"}, {'W', ".--"}, {'X', "-..-"}, {'Y', "-.--"},
    {'Z', "--.."},
    {'0', "-----"}, {'1', ".----"}, {'2', "..---"}, {'3', "...--"}, {'4', "....-"},
    {'5', "....."}, {'6', "-...."}, {'7', "--..."}, {'8', "---.."}, {'9', "----."},
    {'.', ".-.-.-"}, {',', "--..--"}, {'?', "..--.."}, {'!', "-.-.--"},
    {'/', "-..-."}, {'(', "-.--."}, {')', "-.--.-"}, {'&', ".-..."},
    {':', "---..."}, {';', "-.-.-."}, {'=', "-...-"}, {'+', ".-.-."},
    {'-', "-....-"}, {'_', "..--.-"}, {'\"', ".-..-."}, {'@', ".--.-."}
};

unordered_map<string, char> buildReverseMap() {
    unordered_map<string, char> reverseMap;

    for (const auto& pair : MORSE_CODE) {
        reverseMap[pair.second] = pair.first;
    }

    return reverseMap;
}

string toUpperCase(const string& input) {
    string result = input;

    transform(result.begin(), result.end(), result.begin(), [](unsigned char character) {
        return static_cast<char>(toupper(character));
    });

    return result;
}

string encodeToMorse(const string& text) {
    stringstream encoded;
    string upperText = toUpperCase(text);
    bool previousWasSpace = false;

    for (size_t index = 0; index < upperText.length(); ++index) {
        char character = upperText[index];

        if (isspace(static_cast<unsigned char>(character))) {
            if (!previousWasSpace && encoded.tellp() > 0) {
                encoded << " / ";
                previousWasSpace = true;
            }
            continue;
        }

        auto iterator = MORSE_CODE.find(character);

        if (iterator != MORSE_CODE.end()) {
            if (!previousWasSpace && encoded.tellp() > 0) {
                encoded << ' ';
            }

            encoded << iterator->second;
            previousWasSpace = false;
        }
    }

    return encoded.str();
}

string decodeFromMorse(const string& morse) {
    unordered_map<string, char> reverseMorseCode = buildReverseMap();
    stringstream inputStream(morse);
    string token;
    string decoded;

    while (inputStream >> token) {
        if (token == "/") {
            decoded += ' ';
            continue;
        }

        auto iterator = reverseMorseCode.find(token);

        if (iterator != reverseMorseCode.end()) {
            decoded += iterator->second;
        } else {
            decoded += '?';
        }
    }

    return decoded;
}

void saveHistory(const string& operation, const string& input, const string& output) {
    ofstream historyFile("morse_history_cpp.txt", ios::app);

    if (!historyFile) {
        return;
    }

    historyFile << "Operation: " << operation << '\n';
    historyFile << "Input: " << input << '\n';
    historyFile << "Output: " << output << '\n';
    historyFile << string(60, '-') << '\n';
}

void showMenu() {
    cout << "\n==== MorseSignalium C++ ====\n";
    cout << "1. Encode text to Morse\n";
    cout << "2. Decode Morse to text\n";
    cout << "3. Show supported examples\n";
    cout << "4. Exit\n";
    cout << "Choose an option: ";
}

void showExamples() {
    cout << "\nSupported examples:\n";
    cout << "A -> .-\n";
    cout << "B -> -...\n";
    cout << "SOS -> ... --- ...\n";
    cout << "HELLO WORLD -> .... . .-.. .-.. --- / .-- --- .-. .-.. -..\n";
    cout << "Words in Morse must be separated by / when decoding.\n";
}

int main() {
    int option = 0;

    cout << "MorseSignalium C++ Console Application\n";
    cout << "Educational encoder and decoder for Morse code.\n";

    while (true) {
        showMenu();

        if (!(cin >> option)) {
            cout << "Invalid input. Please enter a number.\n";
            cin.clear();
            cin.ignore(10000, '\n');
            continue;
        }

        cin.ignore(10000, '\n');

        if (option == 1) {
            string input;
            cout << "Enter text: ";
            getline(cin, input);

            string output = encodeToMorse(input);
            cout << "Morse: " << output << '\n';
            saveHistory("encode", input, output);
        } else if (option == 2) {
            string input;
            cout << "Enter Morse code: ";
            getline(cin, input);

            string output = decodeFromMorse(input);
            cout << "Text: " << output << '\n';
            saveHistory("decode", input, output);
        } else if (option == 3) {
            showExamples();
        } else if (option == 4) {
            cout << "Exiting MorseSignalium.\n";
            break;
        } else {
            cout << "Unknown option. Please choose 1, 2, 3, or 4.\n";
        }
    }

    return 0;
}
