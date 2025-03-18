import Data.Char
import Data.List
import Data.Bits
import System.IO
import Debug.Trace

sadnums :: [Integer]
sadnums = 1 : 2 : 3 : zipWith (+) (zipWith (+) sadnums (tail sadnums)) (tail (tail sadnums))

insertAt i l x = fs ++ [x] ++ ss
    where (fs,ss) = splitAt i l

perm :: [a] -> [[a]]
perm [] = [[]]
perm [a] = [[a]]
perm (a:as) = do
    p <- perm as
    map (\i -> insertAt i p a) [0..length p]

bitlen :: Integer -> Int
bitlen 0 = 0
bitlen x = 1 + bitlen (div x 2)

bitleni :: Int -> Int
bitleni = bitlen . fromIntegral

combineInts :: [Integer] -> Integer
combineInts [] = 0
combineInts (0:as) = 0b10 + shift (combineInts as) 2
combineInts (a:as) = toInteger k + shift a (bitleni k) + shift (combineInts as) (k + bitleni k)
    where k = bitlen a

chunks :: Int -> [a] -> [[a]]
chunks _ [] = []
chunks n xs =
    let (ys, zs) = splitAt n xs
    in  ys : chunks n zs

checkFlag :: [Int] -> Bool
checkFlag flag = s3 == 972173150824121602412007018285599964790016992331132329938125863396944335343888962496680609453580128670577866680957397079691729409975475808059685839139789293053936863803630038835259562224494784570236168292710615302607612164729087860634163220807870789112490521286338033369715309728573812876856685188727867527120856653286421599271358412318208397826412868064503592632743983056263611708242007057525156038757017150476881049262670633720639217679539166727319119220166210097630306840857360431526039320959828740824636014377722199576160769066945299320633959080096206478867345925976887711848065275698064328942467411250592859159667537686353700866821151556198127062974038263578491639205330066869966234075385650766574939744333009577313203374475753759223187738829176398648444774003773573918200213814722471701473512521111918805562054105666744427883827510528906763939644997500008578015697690376270292284355641125155156907224701171869294855614454339541550163921598724416603467222806157721587368937187858988531852944235542070360977360980827799739300340069386480110250794850173129716283349658574913337784896453484143003637906028298341720507113118885575380276939213158632723560257821715058163323987872940445970564612175876475665670135487735849099061779304884327660652613796429694518398520507159077654634239587076538292695949466015795553278786102331645701154366597632675344998673665278643186259117779275136903303036441544069250977187844586057632073752227909258998380991486165799654172561341265570677993869532339222686006702503505337925872005810399849524956920236896738955238417028174277813326535642322531603659738991191624660615944988880451326461891485195092911605190587405200207449545603910913061343021869416994282431091346921509607742100300679230942667056597634668324180025618607190625349434716104743621199470123360597201555168086638896058048635126143438377562037293263570100912031002597919664811683227890746925407208007478954402284923504175870442143939127275411862327063078947478860177855553501592195814499786085046733962365008782688640410443284131211646936256144067738656739400180204633495276613778683262948663609547633792175874648766430840795657567743648027186726468628882237933244833561527165451196629126779599027458337567998423436738524396139147538627076452521254767431555376828851712305581831709753997902392378170387589134527335894673246849969774103894421767301619928209947259921432787910866219207735230977692967739889689362588179023086424595996141415313116385296549779836418175871808542566198623781963536209298229971517668006887319981280381337183899495887236465054991758400477689974698065664778227707955179748415555655998033154020085186436388288388376592881261748121946038358868094352171801906094159331998555291223712036091522861189558958900369166637712556942296998594658538250283191174386795086613986672942694568879642538403713770630364759813760043547081381539765422635565243503792287941551538390001555468469872873052202842286341651412909285945239689399792817472468335351414494279219845508564410658286844608563368652572689533560292491276512223440542903787463691116929891675690338292505754996329295986628390454605973420547329011278291210044262160345594706889603200553880968013909023568146702980589908370148472467663880696982197118670236082870483339160433530815861984410076731950357240967273435463227473401367382745844743577987994793725544821886240511374227224009976358233849579862082116036155225154815669948712163464988844021527874224480679908079675381017436057959439701662313486227588744016157996312238292713572409592181757371798134114768249260590437372362784546356349335154129508656088828315539661817539999503676328083662516084406305452124669896539310021005292376875096313606997913478220491732968366658503406049200094642112341868168867708860674971988659058088258253440920611675070408364491077162800280130042800770066041786971170440221101374409287257880715739677075399644705278425464881381373708033664540587402331828878951707676460319660646798400680377642680751833999958291661908746139445215553855630238767514730985618189544795209991350944105823954556764959483262380074010938930506836462321555530997305352878587477418089970326030903923711973437911764181825627174892911461666163922655445800578543361435800315525301116006189664364238774278165335067527292851371785950501042244517942107006344764027735542111230961921720339040991664698492448744368776005532107233334184754774839334460591129991208844137410730352209438973573752562494518094648220286324043489409422390837316977361466318129406955081239257149858081603236366951907115955897259618635806370537853585463086321702941139309566964397116335698828109746092092471308372810799256077692055551040620764325827137661650277831984331921822418253242386583635713571124070194077510446846273819784196907578041642212799836575812190872349055188974422227957845227710821188009908746957179663347954043913562105136005672124936301946330286162502314048074418804051514772390152156253827602973951541613233544306594498281398940810909770393962404270422892451086643522640503617608181122338751717141167417352426812676902700698761794059147120784030719204430923771210595946949420400079550605991906162488384126014237952760189074797383417410492438201461789367211739284398200033792936994701400372463455273246895294072129603504338024504640950781318597450075227138630388642481874957764298058565215084567548508009514882672752026624687586979487795147131650247031047338701751644330722366145453977905054486614714856157253653467589211727406553438699913781005882857908423884997254074344287349314844449784282939576414924048843621542066697489736831531243684509225930772777726513108089577839789021453868147769874175388351426741067212873074956905198414773491206034732786521576055567351950283579995806495204636322911507784817002454431891068498335728009089462590630460716679288537935419441327758944590613815577447401252307147028520625878459039255137051138262516994956599572916442085644662336320995372975791697094752419735797061642131447344286511356721040796961846425158309969947253108096262173629425438897497767891008926878604412391273301144472752567378834714693386017746736585368630128559622273022624652304887309889847655189098572097602316404684530082308356622719910652870669326046951025846309259354831363285008381359065005862018315936618757127440078820244861852924898861246485384478018280674624816810935732602099212068025380581458570209110260391462142856473251768038443352852961943204664183537801589356145099091964218438763724911423064888774252976946909532786669151488818180346224760421223890233526491306147116789557515227256616364023941683750522822271151367699763448013959642388239501821531849069488891541282455555163329371092184076932324051414786511911633872145448147565203496632962707929537837218607707149944268866155630520230078813806521730331647147548167050739415697355625394862644737013366678286407877307813174991797490386098729456280305704023155997810949848169175084152955656635858321715636862749958289852373505732159908650818646959475319385043849053447147310625328677562074712420842652696213645336404658965918582775173135568167946216251885271722990607049583321007164466715666243626167326940532696813620342239014030835210365459516754682462205691280595023688700039517164610407315451431572853251606021962238245738967007868482881775584738600571772373214812273655653978936195339203432925939780348122284589879211096550949653136468200425444416270057615020761671775718861199736198850056599985480978053675643944622147277639792030835212495430973779530049648747100873206322795268526661400775628871878746700031703153755249300341473386606825331242050776866794
    where l = length flag
          s1 = take (l*l) $ map ((flag !!) . (fromIntegral :: Integer -> Int) . flip rem (toInteger $ length flag)) sadnums
          s2 = zipWith (\i lst -> perm lst !! i) [0..] $ chunks l s1
          s3 = combineInts $ map (combineInts . map fromIntegral) s2

strToBytes :: String -> [Int]
strToBytes [] = []
strToBytes (a:as) = ord a : strToBytes as

main = do
    putStr "Input flag: "
    hFlush stdout
    flag <- getLine
    putStrLn $ if checkFlag $ strToBytes flag then "Correct" else "Wrong"
