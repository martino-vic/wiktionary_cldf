package com.martinovic.viktor;

import java.io.BufferedWriter;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

/**
 * This class parses the Wiktionary page for category: Old Church Slavonic
 * nouns. It can be also used to parse other Wiktionary pages as long as they
 * contain links with relevant information.
 *
 * @author Tomasz Jastrząb
 * @version 1.0
 */
public class WiktionaryParser {

    private static final String PATH_TO_LANGUAGE_FILE = "lglist.txt";

    public static void main(String[] args) {
        String fileName;
        List<String> languages;
        String[] specialChars = {"ǀ", "À", "ǁ", "ǃ", "Ö", "à", "á", "â", "ã", "ä", "å", "ç", "è", "é", "ê", "ë", "í", "î", "ñ", "ò", "ó", "ô", "õ", "ö", "ù", "ú", "ü"};

        try {
            languages = Files.readAllLines(Paths.get(PATH_TO_LANGUAGE_FILE));
            for (String line : languages) {
                line = line.trim().replace(" ", "_");
                fileName = line.toLowerCase();
                for (String specialChar : specialChars) {
                    line = line.replace(specialChar, URLEncoder.encode(specialChar, "UTF-8"));
                }
                parseAndSave("https://en.wiktionary.org", String.format("/w/index.php?title=Category:%s_lemmas#mw-pages", line), String.format("%s.txt", fileName));
            }
        } catch (IOException ex) {
            Logger.getLogger(WiktionaryParser.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Parses given url and stores the results in the given file
     *
     * @param baseUri base uri of the web site to parse
     * @param url initial url to parse
     * @param outFile path to the output file
     * @throws java.net.MalformedURLException thrown when the URL is incorrect
     * @throws java.io.IOException thrown when the there is some I/O problem
     */
    public static void parseAndSave(String baseUri, String url, String outFile) throws MalformedURLException, IOException {
        Element pagesDiv;
        Document document;
        Elements divs, links;
        Elements nextPageElement;
        String nextPageUrl = baseUri + url;

        try (BufferedWriter bw = Files.newBufferedWriter(Paths.get(outFile),
                Charset.forName("UTF-8"), StandardOpenOption.CREATE, StandardOpenOption.WRITE,
                StandardOpenOption.TRUNCATE_EXISTING)) {
            do {
                document = Jsoup.parse(new URL(nextPageUrl), 3000); // connect to the given url allowing for 3000 ms timeout
                pagesDiv = document.getElementById("mw-pages");
                if(pagesDiv == null) {
                    System.err.println("No pages found for " + outFile + ", please check manually " + nextPageUrl);
                    return;
                }
                divs = document.getElementById("mw-pages").getElementsByClass("mw-category-group"); // this is the class name of the div element enclosing the words
                if(divs.isEmpty()) {
                    System.err.println("No category groups found for " + outFile + ", please check manually: " + nextPageUrl);
                    return;
                }
                for (Element div : divs) { // we iterate over all divs with the above class
                    links = div.getElementsByTag("a"); // we extract links from inside given div
                    for (Element link : links) { // we iterate over links
                        if (link.hasText()) { // if link contains something inside <a> tag
                            bw.write(link.ownText()); // we write just the link text, without possible children
                            bw.newLine(); // new line character
                        }
                    }
                }
                nextPageElement = document.getElementsContainingOwnText("next page"); // we find link to the next page
                if (!nextPageElement.isEmpty() && !nextPageElement.get(0).attr("href").isEmpty()) { // if there is a href element defined
                    nextPageUrl = baseUri + nextPageElement.get(0).attr("href"); // we get the href element
                } else {
                    nextPageUrl = null; // otherwise we finish the loop
                }
            } while (nextPageUrl != null);
        }
    }
}
