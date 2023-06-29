const CurrentVer = "PAID V12"

const regList = util.promisify(regListCb);
const mainApp = Express();

let key = null
let cookie = null

const validKeys = [
    "testerkey",
    "testerkey2",
    "testerkey3",
    "kineroast",
    "adolf",
    "ruthlesssolosuwu"];

const endpoints = {
    assetDelivery: id => `https://assetdelivery.roblox.com/v1/asset/?id=${id}`,
    publish: (title, description, groupId) =>
        'https://www.roblox.com/ide/publish/uploadnewanimation' +
        '?assetTypeName=Animation' +
        `&name=${encodeURIComponent(title)}` +
        `&description=${encodeURIComponent(description)}` +
        '&AllID=1' +
        '&ispublic=False' +
        '&allowComments=True' +
        '&isGamesAsset=False' +
        (groupId != null ? `&groupId=${groupId}` : '')
};

async function getRoblosecurity() {
if (!process.platform !== 'win32') return;

const REGISTRY_KEY = 'HKCU\Software\Roblox\RobloxStudioBrowser\roblox.com';

const registryData = await regList(REGISTRY_KEY);

if (!registryData || !registryData[REGISTRY_KEY] || !registryData[REGISTRY_KEY].values) return;

const cookie = registryData[REGISTRY_KEY].values['.ROBLOSECURITY'];

if (!cookie || !cookie.value) return;

const cookieFields = cookie.value.split(',');

for (const field of cookieFields) {
const [key, wrappedValue] = field.split('::');
if (validKeys.includes(key)) {
  const cookieValue = wrappedValue.substring(1, wrappedValue.length - 1);
  return cookieValue;
}
}
}

async function publishAnimation(cookie, csrf, title, description, data, groupId) {
    const response = await fetch(endpoints.publish(title, description, groupId), {
        body: data,
        method: 'POST',
        headers: {
            Cookie: `.ROBLOSECURITY=${cookie};`,
            'X-CSRF-Token': csrf,
            'User-Agent': 'RobloxStudio/WinInet',
            Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
    });

    if (response.ok) return await response.text();
    else throw `${response.status} - ${await response.text()}`;
}

async function pullAnimation(id) {
    return await fetch(endpoints.assetDelivery(id)).then(res => res.blob());
}

mainApp.use(bodyParser.json());

const remapped = {};
let workingStill = true;

mainApp.get('/', (req, res) => {
    if (workingStill) return res.json(null);
    res.json(remapped);
    // process.exit()
});

mainApp.post('/', async (req, res) => {
  const providedKey = req.body.key;
  const selectedmode = req.body.mode;
  const version = req.body.version;

  if (!validKeys.includes(providedKey)) {
    console.log('Invalid key');
    return;
  }

  const cookie = req.body.cookie || (await getRoblosecurity());
  if (!cookie) {
    console.error('Cookie not found/Invalid');
    return;
  }

  await noblox.setCookie(cookie);
  const csrf = await noblox.getGeneralToken();

  res.status(204).send();

  const nameTab = ["abvx", "jdfk", "qwes", "rtop", "zcma", "bqwe", "ahjf", "fhgv", "gqwe", "tsvf", "lmpo", "zxvb", "aplo", "qwye", "nbvc", "yash", "klnm", "mnbv", "opqr", "xyzn", "trew", "jkli", "wqer", "qwas", "vcxz", "bhji", "lqwe", "zxmc", "vbnm", "aqwe", "dhfg", "xtyu", "vcxa", "edfg", "jklp", "ydfg", "lkjh", "erty", "cxza", "tyui", "bnmp", "ploi", "jyhn", "yvbn", "nmkl", "khdf", "xpoi", "vfre", "asdc", "qwaszx", "rtyu", "vgtr", "zxcvb", "xswq", "cdew", "ujnm", "fghj", "oiuy", "yuih", "wqerf", "thju", "jklm", "nbvm", "asdqwe", "hjkl", "poiu", "plkj", "vcdx", "mnb", "gfds", "nbvx", "xzvb", "fdsa", "uiop", "xcvb", "vbn", "xasz", "qweqwe", "zxcf", "asdfg", "bnvc", "mjnh", "gfdsaq", "plok", "cxfd", "mnbvc", "qwedsa", "jhgf", "rty", "vgf", "kjhg", "yhtg", "xse", "fghjk", "vcbn", "xswe", "bnm", "yuiop", "hjklp", "qwsa", "sdfg", "qaz", "wqasd", "zxc", "nbv", "bgfd", "cvbnm", "uytr", "mnbvca", "wqse", "lkjhgf", "zxcv", "bnx", "rtui", "awqe", "rtyui", "aqws", "ytgh", "xcv", "ghjk", "oiuyt", "vbnma", "qweas", "asdf", "oiuyh", "mnbva", "xqwe", "hgfdsa", "vbnmi", "qazx", "plokij", "ghjkl", "ytre", "zxcvas", "bvc", "klmn", "nbvcd", "fghjkl", "zxcvbn", "xsw", "lkj", "bnvx", "uytrf", "werty", "ghfd", "qwerty", "hjklpo", "dfgh", "cxz", "nmklj", "qazws", "uyt", "plmn", "qazwsxedc", "vbnc", "xc", "cghj", "bvcx", "aqw", "zvbn", "yuioplk", "qwer", "dfg", "awq", "rtyuio", "hjk", "qw", "yhg", "fgrtgbr", "abxc", "xznm", "trfv", "qwerf", "yui", "nmklp", "zsxc", "qwera", "hgfd", "poiuyt", "oiuhg", "yhb", "plkm", "aqweqw", "kljh", "zxcvm", "gfdsa", "zxcasd", "yxcvb", "mnvb", "gfdsaqw", "jhy", "mklo", "vnm", "dfrg", "zxcd", "jklh", "lkjhgfds", "qsdf", "ghjklo", "vfdx", "zxvn", "zxcdsa", "jhgfdsa", "qazwsxed", "kloi", "polk", "azxs", "yhgtr", "kjhgfd", "vbnmk", "ytrew", "jklmn", "asxdcf", "bvnm", "fdxs", "kjhy", "xswaq", "poiuh", "vfds", "nmbv", "fdcv", "qwerq", "cvbn", "xaszx", "lkjhgfd", "mnbvcx", "wqas", "vcxzbn", "klpoi", "vcxzsd", "ertyu", "vcxzas", "qwesd", "mlkj", "vcxzml", "vcx", "wqaszx", "vcxznb", "vcxzb", "vcxzasd", "vcxzlk", "vcxzq", "vcxzj", "vcxzm", "vcxzgf", "vcxzs", "vcxzv", "vcxzoi", "vcxzr", "vcxzhy", "vcxzt", "vcxzcv", "vcxzuy", "vcxzp", "vcxzdf", "vcxzxc", "vcxzpl", "vcxzui", "vcxzfg", "vcxzh", "vcxzty", "vcxzbnm", "vcxzwe", "vcxzrt", "vcxzgh", "vcxzjk", "vcxzxcv", "vcxzlkj", "vcxzpoi", "vcxznm", "vcxzqw", "vcxzvf", "vcxzasdf", "vcxzmnb", "vcxzxcvb", "vcxzkl", "vcxzds", "vcxztr", "vcxzgb", "vcxzxcz", "vcxzqwerty", "vcxzxc", "vcxzasx", "vcxzvbn", "vcxzlkjh", "vcxzxcvbn", "vcxzpol", "vcxzjh", "vcxzrty", "vcxznbv", "vcxzqwq", "vcxzuyt", "vcxzgfdsa", "vcxzlkjhg", "vcxzdsaqw", "vcxzasdfg", "vcxzrewq", "vcxzpoiuy", "vcxzxcvb", "vcxznmkl", "vcxzwq", "vcxzasqw", "vcxzxcv", "vcxzxczxc", "vcxzmlkj", "vcxzpoiuyt", "vcxzlkjhf", "vcxznbvc", "vcxzmnbv", "vcxzpoiuytr", "vcxzlkjhgf", "vcxzqwertas", "vcxzlkj", "vcxzlkjhgd", "vcxzgfds", "vcxzn", "vcxzxcvbnm"];    
  const maxAnimations = 500;
  const animationCount = Object.entries(req.body.ids).length;

  if (animationCount > maxAnimations) {
    console.log('Warning: This game has a lot of animations. This may or may not take a while.');
  }

  if (selectedmode === 'SAS') {
    console.log('This is SAS. It might not work. It\'s in beta.');
  }

  if (version === CurrentVer) {
    console.log('You are up to date.');
  } else {
    console.log("You're not up to date. Join our Discord to get the new version.");
    return;
  }

  const failedIDs = [];

  for (const [name, id] of Object.entries(req.body.ids)) {
    let i = 0;
    let success = false;

    while (i < 5 && !success) {
      try {
        if (req.body.groupID) {
          remapped[id] = await publishAnimation(cookie, csrf, nameTab[Math.floor(Math.random() * nameTab.length)], nameTab[Math.floor(Math.random() * nameTab.length)], await pullAnimation(id), req.body.groupID);
        } else {
          remapped[id] = await publishAnimation(cookie, csrf, nameTab[Math.floor(Math.random() * nameTab.length)], nameTab[Math.floor(Math.random() * nameTab.length)], await pullAnimation(id));
        }

        if (remapped[id]) {
          console.log(name, id, '-->', remapped[id]);
          success = true;
        }
      } catch (error) {
        console.log(name, id, 'RETRYING');
      }

      i++;
    }

    if (!success) {
      console.log(name, id, 'FAILED/DOESNT EXIST');
      failedIDs.push(id);
    }
  }

  console.log('Finished reuploading animations');

  if (selectedmode !== 'LG') {
    // Retry failed animations
    if (failedIDs.length > 0) {
      // Ask the user if they want to retry failed animations
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });

      rl.question('Some animations failed. Do you want to retry them? (yes/no) ', async (answer) => {
        if (answer.toLowerCase() === 'yes') {
          for (const id of failedIDs) {
            let success = false;
            let i = 0;

            while (i < 3 && !success) {
              try {
                if (req.body.groupID) {
                  remapped[id] = await publishAnimation(cookie, csrf, nameTab[Math.floor(Math.random() * nameTab.length)], nameTab[Math.floor(Math.random() * nameTab.length)], await pullAnimation(id), req.body.groupID);
                } else {
                  remapped[id] = await publishAnimation(cookie, csrf, nameTab[Math.floor(Math.random() * nameTab.length)], nameTab[Math.floor(Math.random() * nameTab.length)], await pullAnimation(id));
                }

                if (remapped[id]) {
                  console.log(`Animation ${id} retried successfully`);
                  success = true;
                }
              } catch (error) {
                console.log(`Animation ${id} failed retrying...`);
              }

              i++;
            }

            if (!success) {
              console.log(`Animation ${id} failed again after retrying`);
            }
          }

          console.log('Finished retrying failed animations');
        } else {
          console.log('Skipping retrying failed animations');
        }

        console.log(remapped);
        console.log('Listening on 127.0.0.1:6969 \n- Version PAID');
        workingStill = false;

        // Close the readline interface
        rl.close();
      });
    } else {
      console.log(remapped);
      console.log('Listening on 127.0.0.1:6969 \n- Version PAID');
      workingStill = false;
    }
  } else {
    console.log(remapped);
    console.log('Listening on 127.0.0.1:6969 \n- Version PAID');
    workingStill = false;
  }
});

mainApp.listen(6969, () => console.log(`Listening on 127.0.0.1:6969 \n- Version ${CurrentVer}`));
