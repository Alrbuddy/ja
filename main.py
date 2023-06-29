import sys
import threading
import requests
import os
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QComboBox, QMessageBox, QInputDialog
from http.server import BaseHTTPRequestHandler, HTTPServer

confirmation_file = "confirmation.txt"
current_directory = os.path.dirname(os.path.abspath(__file__))
confirmation_file_path = os.path.join(current_directory, confirmation_file)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(self.server.lua_code.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        lua_code = self.rfile.read(content_length).decode('utf-8')

        self.server.lua_code = lua_code

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Success')

def run_server():
    class CustomRequestHandler(RequestHandler):
        def log_message(self, format, *args):
            pass
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(self.server.lua_code.encode('utf-8'))

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            lua_code = self.rfile.read(content_length).decode('utf-8')

            self.server.lua_code = lua_code

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Success')

    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    httpd.lua_code = ""  
    print('Starting server...')
    httpd.serve_forever()
    
def start_server_thread():
 with open(confirmation_file_path, "w") as file:
    pass

    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    
    
LG_CODE = '''local Version = "PAID V12"
local MarketplaceService = game:GetService("MarketplaceService")
local HttpService = game:GetService("HttpService")
--local HttpEnabled = game:GetService("HttpService").HttpEnabled
--HttpEnabled = true

local function SendPOST(ids, cookie, port, key, mode, version)
    local url = "http://127.0.0.1:" .. port .. "/"
    local data = {
        ids = ids,
        cookie = cookie or nil,
        key = key or "",
        groupID = GroupID or nil,
        mode = Mode or nil,
        version = Version or ""
    }
    HttpService:PostAsync(url, HttpService:JSONEncode(data))
    wait(3)
end

local function PollForResponse(port)
    local response
    while not response do
        response = HttpService:JSONDecode(HttpService:GetAsync("http://127.0.0.1:" .. port .. "/"))
        wait(3)
    end
    return response
end

local function ReturnUUID()
    return tostring(HttpService:GenerateGUID())
end

local function SpoofTable(Table)
    local ids = {}

    for index, v in pairs(Table) do
        local anim = v

        if type(v) == "number" or type(v) == "string" then
            anim = { AnimationId = tostring(v), Name = index }
        elseif anim.ClassName then
            if not anim:IsA("Animation") then
                continue
            end
        end

        local animId = anim.AnimationId:match("%d+")
        if not animId or tonumber(animId) == nil or string.len(animId) <= 6 then
            continue
        end

        local foundAnimInTable = false
        for _, x in pairs(ids) do
            if x == animId then
                foundAnimInTable = true
                break
            end
        end
        if foundAnimInTable then
            continue
        end

        if UserId and ownershipcheck == true or GroupID and ownershipcheck == true then
            local success, productInfo = pcall(function()
                return MarketplaceService:GetProductInfo(animId, Enum.InfoType.Asset)
            end)

            if not success then
                print("Animation does not exist:", animId)
                continue
            end

            if success and productInfo.AssetTypeId == Enum.AssetType.Animation.Value then
                local isOwnedByLocalPlayer = not GroupID and UserId and productInfo.Creator.CreatorTargetId == UserId
                local isOwnedByGroup = GroupID and not UserId and productInfo.Creator.CreatorTargetId == GroupID
                local isOwnedByGroupOrUser = GroupID and UserId and (productInfo.Creator.CreatorTargetId == GroupID or productInfo.Creator.CreatorTargetId == UserId)

                if isOwnedByLocalPlayer then
                    print("Animation", animId, "is created by the local player.")
                    continue
                elseif isOwnedByGroup then
                    print("Animation", animId, "is created by the Group.")
                    continue
                elseif isOwnedByGroupOrUser then
                    print("Animation", animId, "is created by the Group/User.")
                    continue
                end
            end
        end

        if Mode == "Table Spoof and Return 1" or Mode == "Table Spoof and Return 2" then
            ids[index] = animId
        else
            ids[anim.Name .. ReturnUUID()] = animId
        end
    end

    return ids
end

local function GenerateIDList()
    local ids = {}
    if Mode == "LG" then
        ids = SpoofTable(game:GetDescendants())
    end
    return ids
end

if Mode == "Help" then
    for mod, desc in pairs(Modes) do
        print(mod .. " - " .. desc)
    end
    return
end

local idsToGet = GenerateIDList()

while next(idsToGet) do
    local batch = {}
    local count = 0

    for id, value in pairs(idsToGet) do
        count = count + 1
        batch[id] = value

        if count == BatchSize or next(idsToGet, id) == nil then
            local success, errorMsg = pcall(function()
                SendPOST(batch, myCookie, "6969", Key, GroupID, Version)
                local newIDList = PollForResponse("6969")

                if Mode == "LG" then
                    for oldID, newID in pairs(newIDList) do
                        for _, anim in ipairs(game:GetDescendants()) do
                            if anim:IsA("Animation") and string.find(tostring(anim.AnimationId), tostring(oldID)) then
                                local previousId = anim.AnimationId
                                anim.AnimationId = "rbxassetid://" .. tostring(newID)

                                if anim.AnimationId == "rbxassetid://" .. tostring(newID) then
                                    print("Animation ID updated successfully for:", anim.Name)
                                else
                                    print("Failed to update Animation ID for:", anim.Name)
                                    print("Previous ID:", previousId)
                                    print("New ID:", anim.AnimationId)
                                end
                            end
                        end
                    end
                end
            end)

            if not success then
                warn("Error occurred during batch processing:", errorMsg)
            end

         for id in pairs(batch) do
                idsToGet[id] = nil
            end

            count = 0
            batch = {}

            wait(5)
        end
    end
end'''

NOT_LG_CODE = '''local TableSpoof = {}
for i, v in pairs(workspace:GetDescendants()) do
    if v:IsA("PackageLink") then
        v:Destroy()
    end
end

local MarketplaceService = game:GetService("MarketplaceService")
local HttpService = game:GetService("HttpService")
--local HttpEnabled = game:GetService("HttpService").HttpEnabled
--HttpEnabled = true

local Version = "PAID V12"

local function SendPOST(ids, cookie, port, key, mode, version)
    local url = "http://127.0.0.1:" .. port .. "/"
    local data = {
        ids = ids,
        cookie = cookie or nil,
        key = key or "",
        groupID = GroupID or nil,
        mode = Mode or nil,
        version = Version or ""
    }
    HttpService:PostAsync(url, HttpService:JSONEncode(data))
    wait(3)
end

local function PollForResponse(port)
    local response
    while not response do
        response = HttpService:JSONDecode(HttpService:GetAsync("http://127.0.0.1:" .. port .. "/"))
        wait(3)
    end
    return response
end

local function ReturnUUID()
    return tostring(HttpService:GenerateGUID())
end

local function SpoofTable(Table)
    local ids = {}

    for index, v in pairs(Table) do
        local anim = v

        if type(v) == "number" or type(v) == "string" then
            anim = { AnimationId = tostring(v), Name = index }
        elseif anim.ClassName then
            if not anim:IsA("Animation") then
                continue
            end
        end

        local animId = anim.AnimationId:match("%d+")
        if not animId or tonumber(animId) == nil or string.len(animId) <= 6 then
            continue
        end

        local foundAnimInTable = false
        for _, x in pairs(ids) do
            if x == animId then
                foundAnimInTable = true
                break
            end
        end
        if foundAnimInTable then
            continue
        end

        if UserId and ownershipcheck == true or GroupID and ownershipcheck == true then
            local success, productInfo = pcall(function()
                return MarketplaceService:GetProductInfo(animId, Enum.InfoType.Asset)
            end)

            if not success then
                print("Animation does not exist:", animId)
                continue
            end

            if success and productInfo.AssetTypeId == Enum.AssetType.Animation.Value then
                local isOwnedByLocalPlayer = not GroupID and UserId and productInfo.Creator.CreatorTargetId == UserId
                local isOwnedByGroup = GroupID and not UserId and productInfo.Creator.CreatorTargetId == GroupID
                local isOwnedByGroupOrUser = GroupID and UserId and (productInfo.Creator.CreatorTargetId == GroupID or productInfo.Creator.CreatorTargetId == UserId)

                if isOwnedByLocalPlayer then
                    print("Animation", animId, "is created by the local player.")
                    continue
                elseif isOwnedByGroup then
                    print("Animation", animId, "is created by the Group.")
                    continue
                elseif isOwnedByGroupOrUser then
                    print("Animation", animId, "is created by the Group/User.")
                    continue
                end
            end
        end

        if Mode == "Table Spoof and Return 1" or Mode == "Table Spoof and Return 2" then
            ids[index] = animId
        else
            ids[anim.Name .. ReturnUUID()] = animId
        end
    end

    return ids
end

local skipAnims = {
    [507766666] = true,
    [507766951] = true,
    [507766388] = true,
    [507777826] = true,
    [507767714] = true,
    [507784897] = true,
    [507785072] = true,
    [507765000] = true,
    [507767968] = true,
    [507765644] = true,
    [2506281703] = true,
    [507768375] = true,
    [522635514] = true,
    [522638767] = true,
    [507770239] = true,
    [507770453] = true,
    [507771019] = true,
    [507771955] = true,
    [507772104] = true,
    [507776043] = true,
    [507776720] = true,
    [507776879] = true,
    [507777268] = true,
    [507777451] = true,
    [507777623] = true,
    [507770818] = true,
    [507770677] = true,
}

local function SpoofScript(Path)
    local anims = {}
    local scripts = {}
    local marketplaceService = game:GetService("MarketplaceService")

    if Path and Mode == "SSS" then
        scripts = { Path }
    elseif Mode == "SAS" then
        local directories = {
            game.Workspace,
            game.ReplicatedStorage,
            game.ServerScriptService,
            game.ServerStorage,
            game.StarterPlayer.StarterCharacterScripts,
            game.StarterPack,
        }

        for _, directory in ipairs(directories) do
            for _, script in ipairs(directory:GetDescendants()) do
                if script:IsA("LuaSourceContainer") then
                    table.insert(scripts, script)
                end
            end
        end
    end

    for _, script in ipairs(scripts) do
        local source = script.Source
        if not source then
            break
        end
        local tableSource = {}
        for word in source:gmatch("%S+") do
            table.insert(tableSource, word)
        end
        for _, v in ipairs(tableSource) do
            if v and string.match(v, "%d+") and string.len(string.match(v, "%d+")) > 6 then
                local animId = tonumber(v:match("%d+"))

                if ownershipcheck == true then
                    local success, productInfo = pcall(function()
                        return marketplaceService:GetProductInfo(animId, Enum.InfoType.Asset)
                    end)
                    if success and productInfo.AssetTypeId == Enum.AssetType.Animation.Value then
                        if not GroupID and UserId and productInfo.Creator.CreatorTargetId == UserId then
                            print("Animation", animId, "is created by the local player.")
                            break
                        elseif GroupID and not UserId and productInfo.Creator.CreatorTargetId == GroupID then
                            print("Animation", animId, "is created by the Group.")
                            break
                        elseif GroupID and UserId and (productInfo.Creator.CreatorTargetId == GroupID or productInfo.Creator.CreatorTargetId == UserId) then
                            print("Animation", animId, "is created by the Group/User.")
                            break
                        end
                    end
                end

                if skipAnims[animId] then
                    print("Skipping animation", animId, "because it's from Roblox.")
                    break
                end

                anims[animId] = animId
            end
        end
    end

    return anims
end


local function GenerateIDList()
    local ids = {}
    if Mode == "Normal" then
        ids = SpoofTable(game:GetDescendants())
    elseif Mode == "Explorer Selection" then
        ids = SpoofTable(game.Selection:Get())
    elseif Mode == "Table Spoof" then
        if not TableSpoof then
            warn("TableSpoof doesn't exist")
            return
        end
        ids = SpoofTable(TableSpoof)
    elseif Mode == "Table Spoof and Return 1" then
        if not TableSpoof then
            warn("TableSpoof doesn't exist")
            return
        end
        ids = SpoofTable(TableSpoof)
    elseif Mode == "Table Spoof and Return 2" then
        if not TableSpoof then
            warn("TableSpoof doesn't exist")
            return
        end
        ids = SpoofTable(TableSpoof)
    elseif Mode == "SAS" then
        ids = SpoofScript()
    elseif Mode == "SSS" then
        if not ScriptToSpoofPath then
            warn("Please insert the path to the script in the ScriptToSpoofPath variable")
            return
        end
        ids = SpoofScript(ScriptToSpoofPath)
    end
    return ids
end

if Mode == "Help" then
    for mod, desc in pairs(Modes) do
        print(mod .. " - " .. desc)
    end
    return
end

local idsToGet = GenerateIDList()
SendPOST(idsToGet, myCookie, "6969", Key, GroupID, Version)
local newIDList = PollForResponse("6969")

if Mode == "Table Spoof and Return 2" then
    for i, v in ipairs(newIDList) do
        newIDList[i] = "rbxassetid://" .. v
    end
end

if Mode == "Table Spoof and Return 1" or Mode == "Table Spoof and Return 2" then
    print(newIDList)
    return
end

if Mode == "SAS" or Mode == "SSS" then
    local directories = {
        game.Workspace,
        game.ReplicatedStorage,
        game.ServerScriptService,
        game.ServerStorage,
        game.StarterPlayer.StarterCharacterScripts,
        game.StarterPack,
    }

    if Mode == "SAS" then
        for _, directory in ipairs(directories) do
            for _, script in ipairs(directory:GetDescendants()) do
                local scriptType = script.ClassName
                if scriptType == "Script" or scriptType == "ModuleScript" or scriptType == "LocalScript" then
                    local success = false
                    local newSource = ""

                    repeat
                        success, newSource = pcall(function()
                            local source = script.Source
                            for old, new in pairs(newIDList) do
                                source = source:gsub(old, new)
                            end
                            return source
                        end)

                        if success then
                            script.Source = newSource
                        else
                            warn("Failed to update source for", scriptType, "in", script:GetFullName())
                        end
                    until success and script.Source == newSource
                end
            end
        end
    end
end

if Mode == "Normal" or Mode == "Explorer Selection" then
    for oldID, newID in pairs(newIDList) do
        for _, anim in ipairs(game:GetDescendants()) do
            if anim:IsA("Animation") and string.find(tostring(anim.AnimationId), tostring(oldID)) then
                local previousId = anim.AnimationId
                anim.AnimationId = "rbxassetid://" .. tostring(newID)
    
                if anim.AnimationId == "rbxassetid://" .. tostring(newID) then
                    print("Animation ID updated successfully for:", anim.Name)
                else
                    print("Failed to update Animation ID for:", anim.Name)
                    print("Previous ID:", previousId)
                    print("New ID:", anim.AnimationId)
                end
            end
        end
    end
end'''

def spoof_animations():
    userid = userid_entry.text()
    groupid = groupid_entry.text()
    cookie = cookie_entry.text()
    ownership_check = ownership_check_box.isChecked()
    key = key_entry.text()
    mode = mode_combo_box.currentText()

    if cookie == "":
        QMessageBox.warning(window, "Required Field", "Please enter a value for 'My Cookie'.")
        return

    if key == "":
        QMessageBox.warning(window, "Required Field", "Please enter a value for 'Key'.")
        return

    lua_code_table = []
    lua_code_table.append(f'local myCookie = "{cookie}"')
    lua_code_table.append(f'local Key = "{key}"')
    lua_code_table.append(f'local Mode = "{mode}"')
    lua_code_table.append(f'local ownershipcheck = {str(ownership_check).lower()}')

    if userid != "" and groupid != "":
        QMessageBox.warning(window, "Invalid Input", "Please provide either a User ID or a Group ID, not both.")
        return

    if userid != "":
        lua_code_table.append(f'local UserId = {userid}')
        lua_code_table.append('local GroupID = nil')
    elif groupid != "":
        lua_code_table.append('local UserId = nil')
        lua_code_table.append(f'local GroupID = {groupid}')

    if mode == "SSS":
        script_path, ok = QInputDialog.getText(window, "SSS Mode", "Enter the Script to Spoof Path:")
        if ok:
            lua_code_table.append(f'local ScriptToSpoofPath = "{script_path}"')
        else:
            QMessageBox.warning(window, "SSS Mode", "Invalid script path entered.")
            return

    if mode == "LG":
        batch_size, ok = QInputDialog.getInt(window, "LG Mode", "Enter the batch size:")
        if ok:
            if batch_size > 30:
                QMessageBox.warning(window, "LG Mode", "Batch size cannot exceed 30.")
                return
            lua_code_table.append(f'local BatchSize = {batch_size}')
            lua_code_table.append(LG_CODE)
        else:
            QMessageBox.warning(window, "LG Mode", "Invalid batch size entered.")
            return
    else:
        lua_code_table.append(NOT_LG_CODE)

    lua_code = '\n'.join(lua_code_table)
    
    start_server_thread()

    try:
        response = requests.post("http://localhost:8000", data=lua_code.encode('utf-8'))
        if response.status_code == 200:
            QMessageBox.information(window, "Success", "Starting...")
        else:
            QMessageBox.warning(window, "Error", f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        QMessageBox.warning(window, "Error", f"An error occurred: {str(e)}")


def show_mode_info():
    mode = mode_combo_box.currentText()
    if mode == "Normal":
        QMessageBox.information(window, "Mode Information", "Normal mode begins stealing all animations with no filter whatsoever.")
    elif mode == "SAS":
        QMessageBox.information(window, "Mode Information", "SAS mode steals animations only from scripts.")
    elif mode == "SSS":
        QMessageBox.information(window, "Mode Information", "SSS mode steals animations from a specific script.")
    elif mode == "Explorer Selection":
        QMessageBox.information(window, "Mode Information", "Steals the selected animations from the explorer")
    elif mode == "LG":
        QMessageBox.information(window, "Mode Information", "Large game mode Beta testing It basically is compatible with large games nothing else")

def save_changes():
    cookie = cookie_entry.text()
    key = key_entry.text()

    if cookie == "":
        QMessageBox.warning(window, "Required Field", "Please enter a value for 'My Cookie'.")
        return

    if key == "":
        QMessageBox.warning(window, "Required Field", "Please enter a value for 'Key'.")
        return

    settings = QSettings("adolfspoofer", "app")
    settings.setValue("userid", userid_entry.text())
    settings.setValue("groupid", groupid_entry.text())
    settings.setValue("cookie", cookie)
    settings.setValue("ownership_check", ownership_check_box.isChecked())
    settings.setValue("key", key)
    settings.setValue("mode", mode_combo_box.currentText())
    QMessageBox.information(window, "Saved Settings", "Settings have been saved.")

def load_changes():
    settings = QSettings("adolfspoofer", "app")
    userid_entry.setText(settings.value("userid", ""))
    groupid_entry.setText(settings.value("groupid", ""))
    cookie_entry.setText(settings.value("cookie", ""))
    ownership_check_box.setChecked(settings.value("ownership_check", False, type=bool))
    key_entry.setText(settings.value("key", ""))
    mode_combo_box.setCurrentText(settings.value("mode", ""))

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Animation Spoofer")
window.setGeometry(100, 100, 400, 300)

layout = QVBoxLayout()

userid_label = QLabel("User ID:")
userid_entry = QLineEdit()
groupid_label = QLabel("Group ID:")
groupid_entry = QLineEdit()
cookie_label = QLabel("My Cookie:")
cookie_entry = QLineEdit()
ownership_check_box = QCheckBox("Enable Ownership Check")
key_label = QLabel("Key:")
key_entry = QLineEdit()
mode_label = QLabel("Mode:")
mode_combo_box = QComboBox()
mode_combo_box.addItems(["Normal", "SAS", "SSS","Explorer Selection","LG"])
mode_combo_box.currentIndexChanged.connect(show_mode_info)

spoof_button = QPushButton("Spoof Animations")
spoof_button.clicked.connect(spoof_animations)

save_button = QPushButton("Save Changes")
save_button.clicked.connect(save_changes)

load_button = QPushButton("Load Changes")
load_button.clicked.connect(load_changes)

layout.addWidget(userid_label)
layout.addWidget(userid_entry)
layout.addWidget(groupid_label)
layout.addWidget(groupid_entry)
layout.addWidget(cookie_label)
layout.addWidget(cookie_entry)
layout.addWidget(ownership_check_box)
layout.addWidget(key_label)
layout.addWidget(key_entry)
layout.addWidget(mode_label)
layout.addWidget(mode_combo_box)
layout.addWidget(spoof_button)
layout.addWidget(save_button)
layout.addWidget(load_button)

window.setLayout(layout)

load_changes()

window.show()
sys.exit(app.exec_())
