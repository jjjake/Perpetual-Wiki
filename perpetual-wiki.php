<?php
    // If an item list is ready, hand it back, then rename it.
    //  Reset the sleep time to [currently hard-coded] process periodicity.
    // If one is not found, kick off its generation. 
    //  Reset the sleep time to a short interval, to pick up the list.

    require_once '/petabox/setup.inc';    

    header("Content-type: text/plain");    

    ob_implicit_flush(true);
    ob_end_flush();

    // if control file exists, return its contents instead of pinging script
    // this provides a mechanism for overriding default behavior
    $controlFile = "wiki.ctrl";
    if (file_exists($controlFile)==TRUE) {
        readfile($controlFile);
    } else {    
        // $defaultSleep = ...get &defaultSleep=foo arg here :)
        $defaultSleep = "3 months";
        $listFile = "ready_list.txt";
        $lockFile = $listFile.".lck";        
        if (file_exists($listFile)==FALSE) {
            $cmd = "/1/data/ENV/bin/python wiki-d.py";
            $datestamp = date("Ymd");
            exec("{$cmd} >/home/jake/public_html/wiki-dumps/{$datestamp}-stdout_wiki.log 2>&1 &");
            echo "// Started generating list, coming back for it in 1 day...\n";
            echo "## AUTO_SUBMIT_COMMAND=SLEEP=1440 min ##\n";
            echo "## AUTO_SUBMIT_COMMAND=SKIP ##\n";
        } else {
            if (file_exists($lockFile)==TRUE) {
                // while lockfile exists, still being generated...
                echo "// List file exists, but lock file $lockFile indicates not ready; checking back in 60 min...\n";
                echo "## AUTO_SUBMIT_COMMAND=SLEEP=720 min ##\n";
                echo "## AUTO_SUBMIT_COMMAND=SKIP ##\n";
            } else {
                // list ready!
                ob_clean();
                flush();
                $datestamp = date("Ymd");
                $archivalListName = "{$datestamp}-{$listFile}"; 
                echo "// List ready! (Will be archived in $archivalListName)\n";
                echo "// Resetting clock to come back in {$defaultSleep}...\n";
                echo "## AUTO_SUBMIT_COMMAND=SLEEP={$defaultSleep} ##\n";
                readfile($listFile);    
                rename($listFile,$archivalListName);
            }        
        }
    }
?>
